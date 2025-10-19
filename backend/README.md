# Backend - REWIND API

FastAPI backend service for REWIND video processing and AI integration.

## Overview

The backend handles video upload, processing, AI analysis, and VoiceBridge™ narration generation. Built with FastAPI for high performance and async processing.

## Key Technologies

- **FastAPI**: High-performance async web framework
- **TwelveLabs API**: Video scene analysis and object detection
- **Google Gemini**: Natural language generation and translation
- **ElevenLabs**: Voice cloning and speech synthesis
- **Firebase**: Storage and database
- **FFmpeg**: Video and audio processing

## Quick Start

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Run development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Access API documentation at `http://localhost:8000/docs`

## Project Structure

```
backend/
├── app/
│   ├── api/              # API endpoints and routes
│   ├── services/         # External service integrations
│   ├── models/           # Data models and schemas
│   └── utils/            # Helper functions
├── tests/                # Test suite
├── scripts/              # Utility scripts
└── main.py              # Application entry point
```

## Core Services

### Video Processor
Extracts frames and audio from uploaded videos using FFmpeg.

### TwelveLabs Service
Analyzes video content for scenes, objects, people, and actions.

### Gemini Service
Generates natural scene descriptions and handles translation.

### ElevenLabs Service
Manages voice cloning and multilingual speech synthesis for VoiceBridge™.

### Firebase Service
Handles file storage, metadata persistence, and user authentication.

## API Endpoints

- `POST /api/upload` - Upload video for processing
- `GET /api/analysis/{video_id}` - Retrieve analysis results
- `POST /api/narration/generate` - Generate voice narration
- `POST /api/voice-setup/clone` - Clone user voice
- `GET /api/scene-data/{video_id}` - Get scene metadata

## Environment Variables

Required environment variables in `.env`:

```env
TWELVELABS_API_KEY=your_key
GEMINI_API_KEY=your_key
ELEVENLABS_API_KEY=your_key
FIREBASE_PROJECT_ID=your_project
FIREBASE_PRIVATE_KEY=your_key
FIREBASE_CLIENT_EMAIL=your_email
FIREBASE_STORAGE_BUCKET=your_bucket
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test
pytest tests/test_elevenlabs.py -v
```

## Development

### Code Style

- Follow PEP 8
- Use type hints
- Maximum line length: 88 characters
- Run `black` for formatting

### Adding New Endpoints

1. Create route in `app/api/routes/`
2. Add service logic in `app/services/`
3. Define models in `app/models/`
4. Write tests in `tests/`

## Deployment

Deploy to Railway or Render:

```bash
# Railway
railway up

# Or use Docker
docker build -t rewind-backend .
docker run -p 8000:8000 rewind-backend
```

## Performance

- Async/await for non-blocking I/O
- Request batching for AI APIs
- Caching for frequently accessed data
- Database indexing for fast queries

## Troubleshooting

**FFmpeg not found**: Install FFmpeg 6.0+ on your system

**API rate limits**: Check your API quotas on provider dashboards

**Memory issues**: Increase `MAX_VIDEO_SIZE_MB` or process videos in smaller chunks

## Contributing

See main repository [CONTRIBUTING.md](../docs/CONTRIBUTING.md) for guidelines.

## Team

Backend development led by **Joanna Chimalilo** - [GitHub](https://github.com/Jouujo) | [LinkedIn](https://www.linkedin.com/in/joanna-chimalilo-766a15237/)