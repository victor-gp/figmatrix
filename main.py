import os
import tempfile
import base64
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from difflib import SequenceMatcher
import io

# Load environment variables
load_dotenv()

app = FastAPI(title="Speech-to-Text Comparison API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize ElevenLabs client
api_key = os.getenv("ELEVENLABS_API_KEY")
if not api_key:
    raise ValueError("ELEVENLABS_API_KEY environment variable is not set")

client = ElevenLabs(api_key=api_key)

class ComparisonResponse(BaseModel):
    transcript: str
    comparison_text: str
    similarity_score: float
    is_match: bool
    details: Dict[str, Any]

def compare_strings(text1: str, text2: str) -> Dict[str, Any]:
    """Compare two strings and return similarity metrics."""
    # Normalize strings (lowercase, strip whitespace)
    normalized_text1 = text1.lower().strip()
    normalized_text2 = text2.lower().strip()
    
    # Calculate similarity ratio
    similarity_ratio = SequenceMatcher(None, normalized_text1, normalized_text2).ratio()
    
    # Check if they match exactly (ignoring case and whitespace)
    exact_match = normalized_text1 == normalized_text2
    
    # Check if they contain similar content (threshold can be adjusted)
    similarity_threshold = 0.8
    is_similar = similarity_ratio >= similarity_threshold
    
    return {
        "similarity_ratio": similarity_ratio,
        "exact_match": exact_match,
        "is_similar": is_similar,
        "similarity_threshold": similarity_threshold,
        "normalized_transcript": normalized_text1,
        "normalized_comparison": normalized_text2
    }

class SpeechRequest(BaseModel):
    audio_content: str
    comparison_text: str

@app.post("/compare-speech", response_model=ComparisonResponse)
async def compare_speech(request: SpeechRequest):
    """
    Compare speech transcript with provided text using base64 encoded audio content.
    
    Args:
        audio_content: Base64 encoded PCM_s16le_16 audio content
        comparison_text: Text to compare against the transcribed audio
        
    Returns:
        ComparisonResponse containing transcript, comparison result, and similarity metrics
    """
    
    try:
        # Decode base64 audio content
        try:
            audio_bytes = base64.b64decode(request.audio_content)
            print(f"Decoded audio bytes length: {len(audio_bytes)}")
            print(f"Audio data preview: {audio_bytes[:50]}")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid base64 audio content: {str(e)}")
        
        # Create a temporary file to store the decoded audio
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            temp_file.write(audio_bytes)
            temp_file_path = temp_file.name
            print(f"Temporary file created: {temp_file_path}")
        
        try:
            # Convert speech to text using ElevenLabs
            with open(temp_file_path, 'rb') as audio_data:
                print(f"File size: {os.path.getsize(temp_file_path)} bytes")
                response = client.speech_to_text.convert(
                    file=audio_data,
                    file_format="pcm_s16le_16",  # Specify the audio format
                    model_id="scribe_v2"  # You can specify model if needed
                )
                # Extract text from response
                transcript = response.text if hasattr(response, 'text') else str(response)
                print(f"Transcript extracted: '{transcript}'")
            
            # Compare the transcript with the provided text
            comparison_result = compare_strings(transcript, request.comparison_text)
            
            # Prepare response
            response = ComparisonResponse(
                transcript=transcript,
                comparison_text=request.comparison_text,
                similarity_score=comparison_result["similarity_ratio"],
                is_match=comparison_result["exact_match"],
                details=comparison_result
            )
            
            return response
            
        finally:
            # Clean up the temporary file
            os.unlink(temp_file_path)
            
    except Exception as e:
        # Check if it's an ElevenLabs error by checking the error message or module
        if "elevenlabs" in str(type(e)).lower() or "ElevenLabs" in str(e):
            raise HTTPException(status_code=500, detail=f"ElevenLabs API error: {str(e)}")
        else:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Speech-to-Text Comparison API",
        "version": "1.0.0",
        "endpoints": {
            "/compare-speech": "POST - Compare speech transcript with text using base64 encoded audio content",
            "/docs": "GET - Interactive API documentation",
            "/health": "GET - Health check endpoint"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "speech-to-text-comparison-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
