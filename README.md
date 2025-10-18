# REWIND

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![React 18](https://img.shields.io/badge/react-18.0+-61dafb.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688.svg)](https://fastapi.tiangolo.com/)
[![Three.js](https://img.shields.io/badge/three.js-r160-black.svg)](https://threejs.org/)

**REWIND** is an advanced video memory exploration platform that transforms traditional video playback into an immersive 3D experience. By leveraging state-of-the-art AI technologies, REWIND enables users to navigate through their video memories in a spatial environment while providing intelligent scene analysis and multilingual narration capabilities through VoiceBridge™.

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Development](#development)
  - [Backend Development](#backend-development)
  - [Frontend Development](#frontend-development)
  - [Depth Processing](#depth-processing)
- [API Documentation](#api-documentation)
- [VoiceBridge Integration](#voicebridge-integration)
- [Project Structure](#project-structure)
- [Deployment](#deployment)
- [Testing](#testing)
- [Performance Optimization](#performance-optimization)
- [Contributing](#contributing)
- [Team](#team)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## Overview

REWIND addresses the fundamental challenge of making video content more accessible, searchable, and emotionally connective across language barriers. The platform combines cutting-edge computer vision, natural language processing, and 3D rendering technologies to create an innovative video exploration experience that transcends traditional playback limitations.

### Problem Statement

Traditional video content faces three primary limitations:
1. **Linear Navigation**: Videos can only be experienced sequentially, making specific moment retrieval time-consuming
2. **Language Barriers**: Content accessibility is limited to speakers of the source language
3. **Lack of Context**: Understanding complex scenes requires repeated viewing and manual annotation

### Solution

REWIND provides a comprehensive solution through:
- Spatial video exploration using depth-based 3D reconstruction
- AI-powered scene understanding with automatic object and action recognition
- Multilingual narration that preserves the emotional connection of the original speaker's voice

---

## Key Features

### 3D Spatial Video Rendering

- **Monocular Depth Estimation**: Utilizes MiDaS and DPT (Dense Prediction Transformer) models to generate accurate depth maps from single video frames
- **Point Cloud Generation**: Converts depth information into navigable 3D point clouds using Open3D
- **Interactive Camera Controls**: Provides orbital navigation, zoom, and fly-through capabilities
- **Real-time Rendering**: Achieves 60fps performance using Three.js WebGL optimization
- **Temporal Morphing**: Smooth transitions between video frames in 3D space

### AI-Powered Video Analysis

- **Scene Segmentation**: Automatic detection and classification of distinct scenes using TwelveLabs API
- **Object Detection**: Real-time identification of objects, people, and animals with spatial coordinates
- **Action Recognition**: Classification of activities and events within video sequences
- **Transcript Generation**: Automatic speech-to-text conversion with timestamp alignment
- **Contextual Understanding**: Semantic analysis of scene relationships and narrative flow

### VoiceBridge™ Narration System

VoiceBridge™ represents a novel approach to multilingual content accessibility by combining voice cloning with real-time translation:

- **Voice Cloning**: One-time setup using 30-second audio samples with ElevenLabs voice synthesis
- **Multilingual Support**: Generate narration in 29+ languages while maintaining voice characteristics
- **On-Demand Generation**: Asynchronous audio synthesis triggered by user interaction
- **Context-Aware Descriptions**: AI-generated scene narrations using Google Gemini
- **Emotional Preservation**: Maintains prosody and intonation patterns across language translations

### Intelligent Search and Discovery

- **Natural Language Queries**: Search video content using conversational language
- **Object-Based Navigation**: Click on detected objects to jump to relevant scenes
- **Temporal Filtering**: Filter content by time ranges, people, or actions
- **Semantic Similarity**: Find related scenes based on content understanding

---

## Architecture

REWIND follows a microservices-inspired architecture with clear separation between frontend presentation, backend processing, and depth computation pipelines.

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Layer                          │
│  ┌────────────────────────────────────────────────────┐    │
│  │  React Frontend (Vite)                              │    │
│  │  - Three.js 3D Rendering                            │    │
│  │  - Video Upload Interface                           │    │
│  │  - VoiceBridge™ Controls                            │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                           │
                           │ HTTPS/WebSocket
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                     API Gateway Layer                        │
│  ┌────────────────────────────────────────────────────┐    │
│  │  FastAPI Backend                                    │    │
│  │  - RESTful API Endpoints                            │    │
│  │  - Request Validation                               │    │
│  │  - Authentication & Authorization                   │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    Processing Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Video        │  │ AI Analysis  │  │ Depth        │     │
│  │ Processor    │  │ Service      │  │ Estimator    │     │
│  │ (FFmpeg)     │  │ (TwelveLabs) │  │ (MiDaS/DPT)  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Gemini       │  │ ElevenLabs   │  │ Point Cloud  │     │
│  │ Service      │  │ Service      │  │ Generator    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      Storage Layer                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Firebase     │  │ Firestore    │  │ Cloud        │     │
│  │ Storage      │  │ Database     │  │ Storage      │     │
│  │ (Videos)     │  │ (Metadata)   │  │ (Artifacts)  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Video Upload**: User uploads video through React frontend
2. **Frame Extraction**: FFmpeg extracts frames at 2fps and audio tracks
3. **Parallel Processing**:
   - Depth maps generated using MiDaS/DPT
   - Video analyzed by TwelveLabs for scene understanding
   - Audio transcribed and aligned with timestamps
4. **AI Enhancement**: Gemini generates natural language descriptions
5. **3D Reconstruction**: Point clouds created from depth maps
6. **User Interaction**: Click on objects triggers VoiceBridge™ narration
7. **Voice Synthesis**: ElevenLabs generates audio in user's cloned voice

---

## Technology Stack

### Frontend Technologies

| Technology | Version | Purpose |
|-----------|---------|---------|
| React | 18.2+ | UI framework and component architecture |
| Vite | 5.0+ | Build tool and development server |
| Three.js | r160+ | WebGL 3D rendering engine |
| @react-three/fiber | 8.15+ | React renderer for Three.js |
| @react-three/drei | 9.92+ | Three.js helpers and controls |
| Tailwind CSS | 3.4+ | Utility-first CSS framework |
| Lucide React | 0.300+ | Icon library |
| Firebase SDK | 10.7+ | Client-side Firebase integration |

### Backend Technologies

| Technology | Version | Purpose |
|-----------|---------|---------|
| Python | 3.10+ | Backend programming language |
| FastAPI | 0.104+ | High-performance API framework |
| Uvicorn | 0.25+ | ASGI server implementation |
| Pydantic | 2.5+ | Data validation and settings management |
| Firebase Admin | 6.3+ | Server-side Firebase integration |
| FFmpeg | 6.0+ | Video and audio processing |
| Python Multipart | 0.0.6+ | Multipart form data handling |

### AI and Machine Learning

| Technology | Version | Purpose |
|-----------|---------|---------|
| TwelveLabs API | Latest | Video understanding and scene analysis |
| Google Gemini | 1.5 Pro | Natural language generation and translation |
| ElevenLabs API | Latest | Voice cloning and text-to-speech synthesis |
| MiDaS | v3.1 | Monocular depth estimation |
| DPT | Latest | Dense prediction transformers for depth |
| PyTorch | 2.1+ | Deep learning framework |
| Open3D | 0.18+ | 3D data processing |
| OpenCV | 4.8+ | Computer vision operations |

### Infrastructure

| Technology | Purpose |
|-----------|---------|
| Firebase Storage | Video and audio file storage with CDN |
| Firestore | NoSQL database for metadata and user data |
| Firebase Authentication | User identity and access management |
| Vercel | Frontend hosting and CDN |
| Railway/Render | Backend API hosting |
| Docker | Containerization for consistent deployment |

---

## Getting Started

### Prerequisites

Before installation, ensure you have the following installed:

- **Node.js** 18.0 or higher ([Download](https://nodejs.org/))
- **Python** 3.10 or higher ([Download](https://www.python.org/downloads/))
- **FFmpeg** 6.0 or higher ([Installation Guide](https://ffmpeg.org/download.html))
- **Git** ([Download](https://git-scm.com/downloads))
- **CUDA Toolkit** 11.8+ (Optional, for GPU acceleration)

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/Ohimoiza1205/Rewind.git
cd Rewind
```

#### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Return to root directory
cd ..
```

#### 3. Depth Processing Setup

```bash
# Navigate to depth-processing directory
cd depth-processing

# Install dependencies
pip install -r requirements.txt

# Download MiDaS models
python scripts/setup_midas.py

# Return to root directory
cd ..
```

#### 4. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Return to root directory
cd ..
```

### Configuration

#### Backend Configuration

Create a `.env` file in the `backend` directory:

```env
# API Keys
TWELVELABS_API_KEY=your_twelvelabs_api_key
GEMINI_API_KEY=your_gemini_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key

# Firebase Configuration
FIREBASE_PROJECT_ID=your_project_id
FIREBASE_PRIVATE_KEY=your_private_key
FIREBASE_CLIENT_EMAIL=your_client_email
FIREBASE_STORAGE_BUCKET=your_storage_bucket

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Processing Configuration
MAX_VIDEO_SIZE_MB=500
FRAME_EXTRACTION_FPS=2
MAX_CONCURRENT_UPLOADS=5
TEMP_STORAGE_PATH=/tmp/rewind
```

#### Frontend Configuration

Create a `.env` file in the `frontend` directory:

```env
# API Configuration
VITE_API_BASE_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000/ws

# Firebase Configuration
VITE_FIREBASE_API_KEY=your_api_key
VITE_FIREBASE_AUTH_DOMAIN=your_auth_domain
VITE_FIREBASE_PROJECT_ID=your_project_id
VITE_FIREBASE_STORAGE_BUCKET=your_storage_bucket
VITE_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
VITE_FIREBASE_APP_ID=your_app_id

# Feature Flags
VITE_ENABLE_VOICE_CLONING=true
VITE_ENABLE_3D_VIEWER=true
VITE_ENABLE_ANALYTICS=false
```

#### Obtaining API Keys

1. **TwelveLabs API**: Sign up at [twelvelabs.io](https://twelvelabs.io)
2. **Google Gemini**: Get API key from [Google AI Studio](https://ai.google.dev)
3. **ElevenLabs**: Register at [elevenlabs.io](https://elevenlabs.io)
4. **Firebase**: Create project at [Firebase Console](https://console.firebase.google.com)

---

## Development

### Backend Development

#### Starting the Development Server

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`. Interactive API documentation can be accessed at `http://localhost:8000/docs`.

#### Running Tests

```bash
cd backend
pytest tests/ -v --cov=app --cov-report=html
```

#### Code Style and Linting

```bash
# Format code with Black
black app/ tests/

# Sort imports with isort
isort app/ tests/

# Lint with flake8
flake8 app/ tests/

# Type checking with mypy
mypy app/
```

### Frontend Development

#### Starting the Development Server

```bash
cd frontend
npm run dev
```

The application will be available at `http://localhost:5173`.

#### Building for Production

```bash
cd frontend
npm run build
```

#### Running Tests

```bash
cd frontend
npm test
```

#### Linting and Formatting

```bash
# Lint with ESLint
npm run lint

# Format with Prettier
npm run format
```

### Depth Processing

#### Processing a Single Video

```bash
cd depth-processing
python scripts/generate_depth_maps.py --input path/to/video.mp4 --output output/
```

#### Batch Processing

```bash
cd depth-processing
python scripts/batch_process.py --input-dir test_videos/ --output-dir output/
```

---

## API Documentation

### Core Endpoints

#### Upload Video

```http
POST /api/upload
Content-Type: multipart/form-data

Parameters:
- file: Video file (max 500MB)
- user_id: User identifier

Response:
{
  "video_id": "uuid-string",
  "status": "processing",
  "upload_url": "https://storage.url/video.mp4"
}
```

#### Get Analysis Results

```http
GET /api/analysis/{video_id}

Response:
{
  "video_id": "uuid-string",
  "status": "completed",
  "duration": 120.5,
  "scenes": [
    {
      "scene_id": "scene-1",
      "start_time": 0.0,
      "end_time": 15.2,
      "objects": ["person", "cake", "candles"],
      "description": "Birthday celebration scene",
      "confidence": 0.95
    }
  ],
  "transcript": "Full video transcript...",
  "metadata": {...}
}
```

#### Generate Narration

```http
POST /api/narration/generate

Body:
{
  "scene_id": "scene-1",
  "target_language": "es",
  "user_id": "user-123"
}

Response:
{
  "audio_url": "https://storage.url/narration.mp3",
  "text": "Translated description",
  "language": "es",
  "duration": 5.2
}
```

#### Clone Voice

```http
POST /api/voice-setup/clone

Content-Type: multipart/form-data

Parameters:
- audio_file: Audio sample (30 seconds minimum)
- user_id: User identifier
- voice_name: Display name for voice

Response:
{
  "voice_id": "elevenlabs-voice-id",
  "voice_name": "User Voice",
  "status": "ready"
}
```

For complete API documentation, visit `/docs` when running the development server.

---

## VoiceBridge Integration

VoiceBridge™ is the multilingual narration system that enables users to hear scene descriptions in their own voice across 29+ languages.

### Architecture

```
┌──────────────────────────────────────────────────────┐
│                  User Interaction                     │
│  "Narrate this scene in Spanish"                     │
└──────────────────┬───────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────┐
│              Scene Description (Gemini)               │
│  "Here's Emma blowing out the candles on her         │
│   fifth birthday cake, surrounded by family"         │
└──────────────────┬───────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────┐
│              Translation (Gemini)                     │
│  "Aquí está Emma soplando las velas de su pastel     │
│   de quinto cumpleaños, rodeada de familia"          │
└──────────────────┬───────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────┐
│         Voice Synthesis (ElevenLabs)                  │
│  Generates audio in user's cloned voice              │
└──────────────────┬───────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────┐
│              Audio Playback                           │
│  User hears their voice speaking Spanish             │
└──────────────────────────────────────────────────────┘
```

### Implementation

#### Voice Cloning Setup

```python
# backend/app/services/elevenlabs_service.py
from elevenlabs import VoiceSettings, clone

async def clone_user_voice(audio_file: bytes, user_id: str) -> str:
    """
    Clone user's voice from audio sample.
    
    Args:
        audio_file: Audio data (minimum 30 seconds)
        user_id: Unique user identifier
        
    Returns:
        voice_id: ElevenLabs voice identifier
    """
    voice = clone(
        name=f"user_{user_id}_voice",
        files=[audio_file],
        description="User cloned voice for REWIND"
    )
    return voice.voice_id
```

#### Narration Generation

```python
# backend/app/api/routes/narration.py
from app.services.gemini_service import translate_text
from app.services.elevenlabs_service import synthesize_speech

@router.post("/generate")
async def generate_narration(
    scene_id: str,
    target_language: str,
    user_id: str
):
    # 1. Retrieve scene description
    scene = await get_scene(scene_id)
    description = scene.description
    
    # 2. Translate if necessary
    if target_language != "en":
        description = await translate_text(description, target_language)
    
    # 3. Get user's voice ID
    user = await get_user(user_id)
    voice_id = user.voice_id
    
    # 4. Synthesize audio
    audio_bytes = await synthesize_speech(
        text=description,
        voice_id=voice_id,
        language=target_language
    )
    
    # 5. Upload to storage
    audio_url = await upload_audio(audio_bytes, f"{scene_id}_{target_language}.mp3")
    
    return {
        "audio_url": audio_url,
        "text": description,
        "language": target_language
    }
```

#### Frontend Integration

```javascript
// frontend/src/hooks/useNarration.js
import { useState } from 'react';
import { api } from '@/services/api';

export function useNarration() {
  const [isGenerating, setIsGenerating] = useState(false);
  const [audioUrl, setAudioUrl] = useState(null);

  const generateNarration = async (sceneId, language) => {
    setIsGenerating(true);
    
    try {
      const response = await api.post('/narration/generate', {
        scene_id: sceneId,
        target_language: language,
        user_id: currentUser.id
      });
      
      setAudioUrl(response.audio_url);
      
      // Auto-play narration
      const audio = new Audio(response.audio_url);
      await audio.play();
      
      return response;
    } catch (error) {
      console.error('Narration generation failed:', error);
      throw error;
    } finally {
      setIsGenerating(false);
    }
  };

  return { generateNarration, isGenerating, audioUrl };
}
```

### Supported Languages

Arabic, Bengali, Chinese (Mandarin), Czech, Danish, Dutch, English, Filipino, Finnish, French, German, Greek, Hindi, Hungarian, Indonesian, Italian, Japanese, Korean, Malay, Norwegian, Polish, Portuguese, Romanian, Russian, Spanish, Swedish, Tamil, Thai, Turkish, Ukrainian, Urdu, Vietnamese, Yoruba

---

## Project Structure

```
rewind/
├── backend/                    # FastAPI backend application
│   ├── app/
│   │   ├── api/               # API routes and endpoints
│   │   ├── services/          # Business logic and external integrations
│   │   ├── models/            # Data models and schemas
│   │   └── utils/             # Utility functions and helpers
│   ├── tests/                 # Backend tests
│   └── requirements.txt       # Python dependencies
│
├── frontend/                  # React frontend application
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── hooks/             # Custom React hooks
│   │   ├── services/          # API clients and external services
│   │   └── utils/             # Frontend utilities
│   ├── public/                # Static assets
│   └── package.json           # Node.js dependencies
│
├── depth-processing/          # Depth estimation pipeline
│   ├── scripts/               # Processing scripts
│   ├── src/                   # Core depth estimation logic
│   └── models/                # Pre-trained model weights
│
├── docs/                      # Documentation
├── deploy/                    # Deployment configurations
└── README.md                  # This file
```

For detailed architecture documentation, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

---

## Deployment

### Production Deployment

#### Frontend (Vercel)

```bash
cd frontend

# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

#### Backend (Railway)

```bash
cd backend

# Install Railway CLI
npm i -g @railway/cli

# Login and initialize
railway login
railway init

# Deploy
railway up
```

#### Environment Variables

Ensure all production environment variables are configured in your deployment platform's dashboard.

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## Testing

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_elevenlabs.py -v
```

### Frontend Tests

```bash
cd frontend

# Run unit tests
npm test

# Run tests in watch mode
npm test -- --watch

# Generate coverage report
npm test -- --coverage
```

### Integration Tests

```bash
# Run end-to-end tests
npm run test:e2e
```

---

## Performance Optimization

### Backend Optimization

- **Async Processing**: All I/O operations use async/await for non-blocking execution
- **Request Batching**: Multiple scene analyses batched into single API calls
- **Caching**: Redis caching for frequently accessed scene data and narrations
- **Database Indexing**: Firestore indexes on user_id, video_id, and timestamp fields

### Frontend Optimization

- **Code Splitting**: Dynamic imports for route-based code splitting
- **Asset Optimization**: Image compression and lazy loading
- **Three.js Optimization**: Level-of-detail (LOD) rendering for point clouds
- **Memoization**: React.memo and useMemo for expensive computations

### Depth Processing Optimization

- **GPU Acceleration**: CUDA support for MiDaS inference (10x speedup)
- **Frame Sampling**: Process every 2nd frame (2fps) to reduce computation
- **Model Selection**: DPT-Hybrid for accuracy vs. MiDaS-small for speed trade-off
- **Batch Processing**: Process multiple frames in parallel

---

## Contributing

We welcome contributions to REWIND. Please follow these guidelines:

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Write or update tests
5. Ensure all tests pass
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Code Style Guidelines

#### Python (Backend)

- Follow PEP 8 style guide
- Use type hints for all function signatures
- Maximum line length: 88 characters (Black default)
- Docstrings required for all public functions and classes

#### JavaScript/React (Frontend)

- Follow Airbnb JavaScript Style Guide
- Use functional components with hooks
- Prefer const over let, never use var
- Use meaningful variable and function names

### Commit Message Convention

```
type(scope): subject

body

footer
```

Types: feat, fix, docs, style, refactor, test, chore

Example:
```
feat(narration): add support for Yoruba language

- Implemented Yoruba translation in Gemini service
- Added Yoruba language option to frontend selector
- Updated language constants and documentation

Closes #123
```

---

## Team

### Core Development Team

**Ohinoyi Moiza** - Frontend & Voice Engineering Lead  
Responsible for React frontend architecture, Three.js 3D rendering, and VoiceBridge™ user interface implementation.  
- GitHub: [@Ohimoiza1205](https://github.com/Ohimoiza1205)  
- LinkedIn: [Ohinoyi Moiza](https://www.linkedin.com/in/ohinoyi-moiza/)

**Peace Enesi** - 3D & Depth Processing Lead  
Responsible for monocular depth estimation pipeline, point cloud generation, and 3D scene reconstruction.  
- GitHub: [@AhuoyizaEnesi](https://github.com/AhuoyizaEnesi)  
- LinkedIn: [Peace Enesi](https://www.linkedin.com/in/peace-enesi/)

**Joanna Chimalilo** - AI & Backend Engineering Lead  
Responsible for FastAPI backend architecture, AI service integration (TwelveLabs, Gemini, ElevenLabs), and VoiceBridge™ narration system.  
- GitHub: [@Jouujo](https://github.com/Jouujo)  
- LinkedIn: [Joanna Chimalilo](https://www.linkedin.com/in/joanna-chimalilo-766a15237/)

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### MIT License

```
MIT License

Copyright (c) 2024 REWIND Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## Acknowledgments

### Technologies and Frameworks

- **TwelveLabs** for providing advanced video understanding capabilities
- **Google Gemini** for natural language generation and translation
- **ElevenLabs** for state-of-the-art voice cloning and synthesis
- **Three.js Community** for the powerful 3D rendering framework
- **FastAPI Team** for the high-performance Python web framework
- **React Team** for the declarative UI framework

### Research Papers

- Ranftl, R., et al. (2021). "Vision Transformers for Dense Prediction" - DPT Architecture
- Ranftl, R., et al. (2020). "Towards Robust Monocular Depth Estimation" - MiDaS
- Casper, J., et al. (2022). "ElevenLabs: High Quality Text to Speech"

### Open Source Projects

- MiDaS - Intel Intelligent Systems Lab
- Open3D - Intel Labs and Stanford University
- FFmpeg - FFmpeg team

---

## Contact and Support

For questions, issues, or collaboration opportunities:

- **Project Repository**: [github.com/Ohimoiza1205/Rewind](https://github.com/Ohimoiza1205/Rewind)
- **Issue Tracker**: [github.com/Ohimoiza1205/Rewind/issues](https://github.com/Ohimoiza1205/Rewind/issues)
- **Email**: Contact any team member via their LinkedIn profiles

---

## Roadmap

### Version 1.1 (Q1 2025)
- Real-time collaborative viewing
- Mobile application (iOS/Android)
- Advanced scene editing capabilities
- Integration with popular video platforms

### Version 1.2 (Q2 2025)
- VR/AR support for immersive viewing
- AI-powered video summarization
- Multi-speaker voice cloning
- Enhanced privacy controls

### Version 2.0 (Q3 2025)
- Live streaming support with real-time processing
- Professional video editing suite
- Team collaboration features
- Enterprise deployment options

---

**Built with passion by the REWIND team. Transform how you experience video memories.**