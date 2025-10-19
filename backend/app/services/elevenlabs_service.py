import requests
from app.config import settings

ELEVENLABS_API_URL = "https://api.elevenlabs.io/v1"

def get_available_voices():
    """Get list of available voices"""
    headers = {
        "xi-api-key": settings.ELEVENLABS_API_KEY
    }
    
    response = requests.get(
        f"{ELEVENLABS_API_URL}/voices",
        headers=headers
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"ElevenLabs API error: {response.status_code} - {response.text}")

def text_to_speech(text: str, voice_id: str = None) -> bytes:
    """Convert text to speech audio"""
    
    # Use default voice if none provided
    if not voice_id:
        # Get first available voice
        voices = get_available_voices()
        voice_id = voices['voices'][0]['voice_id']
    
    headers = {
        "xi-api-key": settings.ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    
    response = requests.post(
        f"{ELEVENLABS_API_URL}/text-to-speech/{voice_id}",
        headers=headers,
        json=data
    )
    
    if response.status_code == 200:
        return response.content  # Returns audio bytes
    else:
        raise Exception(f"ElevenLabs API error: {response.status_code} - {response.text}")

def save_audio_file(audio_bytes: bytes, filename: str) -> str:
    """Save audio bytes to file"""
    filepath = f"app/data/temp/{filename}"
    
    with open(filepath, 'wb') as f:
        f.write(audio_bytes)
    
    return filepath
