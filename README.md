# Speech-to-Text Comparison API

A FastAPI application that receives PCM audio files, transcribes them using ElevenLabs, and compares the transcript with a provided text string.

## Features

- Accept base64 encoded PCM audio content via query parameters
- Convert speech to text using ElevenLabs API
- Compare transcript with provided text
- Return similarity scores and match results
- RESTful API with interactive documentation

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your ElevenLabs API key
   ```

3. **Get an ElevenLabs API key:**
   - Sign up at [ElevenLabs](https://elevenlabs.io/)
   - Get your API key from the dashboard
   - Add it to your `.env` file

## Running the Application

```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### POST /compare-speech

Compare speech transcript with provided text using base64 encoded audio content.

**Request:**
- Method: POST
- Parameters (query parameters):
  - `audio_content`: Base64 encoded PCM_s16le_16 audio content (required)
  - `comparison_text`: Text to compare against transcript (required)

**Example using curl:**
```bash
# First encode your PCM file to base64
AUDIO_BASE64=$(base64 -w 0 audio.pcm)

curl -X POST "http://localhost:8000/compare-speech?audio_content=$AUDIO_BASE64&comparison_text=Hello world, this is a test"
```

**JavaScript/Frontend Example:**
```javascript
// Convert audio file to base64
function fileToBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => {
            // Remove the data URL prefix (e.g., "data:audio/pcm;base64,")
            const base64 = reader.result.split(',')[1];
            resolve(base64);
        };
        reader.onerror = error => reject(error);
    });
}

// Make API call
async function compareSpeech(audioFile, comparisonText) {
    const audioBase64 = await fileToBase64(audioFile);
    
    const response = await fetch(`http://localhost:8000/compare-speech?audio_content=${audioBase64}&comparison_text=${encodeURIComponent(comparisonText)}`, {
        method: 'POST'
    });
    
    return await response.json();
}
```

**Response:**
```json
{
  "transcript": "hello world this is a test",
  "comparison_text": "Hello world, this is a test",
  "similarity_score": 0.95,
  "is_match": false,
  "details": {
    "similarity_ratio": 0.95,
    "exact_match": false,
    "is_similar": true,
    "similarity_threshold": 0.8,
    "normalized_transcript": "hello world this is a test",
    "normalized_comparison": "hello world this is a test"
  }
}
```

### GET /

Root endpoint with API information.

### GET /health

Health check endpoint.

## API Documentation

Interactive documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Comparison Logic

The API performs string comparison with the following metrics:

- **similarity_ratio**: Float between 0 and 1 using SequenceMatcher
- **exact_match**: Boolean indicating exact match (ignoring case and whitespace)
- **is_similar**: Boolean indicating if similarity ratio >= 0.8
- **similarity_threshold**: Currently set to 0.8 (configurable)

## Error Handling

The API returns appropriate HTTP status codes and error messages for:
- Invalid file types
- Missing required parameters
- ElevenLabs API errors
- Internal server errors

## Dependencies

- FastAPI: Web framework
- Uvicorn: ASGI server
- ElevenLabs: Speech-to-text API client
- python-dotenv: Environment variable management
- python-multipart: File upload support
