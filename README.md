# Speech Therapy app

## Overview

This app is an interactive speech therapy application designed to help children with speech issues practice pronunciation of challenging sounds through tongue twisters and targeted sentences. The application provides real-time feedback on pronunciation accuracy by comparing spoken words against expected text.

### How It Works

- **Sentence Display**: The application presents sentences and tongue twisters tailored to specific speech sounds that children struggle with.
- **Interactive Practice**: Users speak each word into their device's microphone, with visual guidance showing which word to pronounce next.
- **Space Bar Navigation**: Press the space bar between words to move the "cursor" to the next word in the sequence.
- **Real-time Validation**: Your pronunciation is instantly validated against the expected word using advanced speech recognition technology.
- **Instant Feedback**: Receive feedback on whether your pronunciation matches the target word, helping you improve over time.

### Target Audience

This application is specifically designed for:

- Speech-language pathologists and therapists
- Children with speech articulation disorders

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js (for frontend development)
- ElevenLabs API account and API key

### Installation

1. Clone the repository
2. Install backend dependencies: `pip install -r requirements.txt`
3. Install frontend dependencies: `cd frontend && npm install`
4. Set up your ElevenLabs API key on `.env.example`
5. Start the backend server: `python main.py`
6. Start the frontend development server: `cd frontend && npm run dev`

### Usage

1. Open the application in your web browser
2. Allow microphone access when prompted
3. Select a tongue twister or sentence to practice
4. Speak each word clearly into your microphone
5. Press space bar to advance to the next word
6. Receive instant feedback on your pronunciation accuracy

## Stack

### APIs & Services

- **ElevenLabs Speech-to-Text API** - Converts spoken audio to text for comparison
- **Web Audio API** - Captures microphone input from the browser

### Backend

- **ElevenLabs Python SDK** - Interface for speech-to-text conversion
- **Python 3.x** - Core programming language
- **FastAPI** - Modern, fast web framework for building APIs

### Frontend

- **HTML5** - Structure and semantics
- **CSS3** - Styling and responsive design
- **JavaScript/TypeScript** - Client-side interactivity
- **Vite** - Build tool and development server
- **React** - User interface components

### Key Features

- **Real-time Speech Recognition**: Leverages ElevenLabs' advanced speech-to-text technology
- **Pronunciation Comparison**: Sophisticated string matching algorithms with configurable similarity thresholds
- **Progressive Word Navigation**: Space bar controlled word-by-word progression
- **Responsive Design**: Works across desktop and mobile devices
- **Audio Processing**: Handles PCM audio encoding and decoding
- **Error Handling**: Robust error management for various speech recognition scenarios

## The Team

- **Afaf Driouech**
- **Daniele Pala**
- **Rahimakhan Abduqodirova**
- **Thao Phuong Pham**
- **Victor Gonzalez Prieto**
