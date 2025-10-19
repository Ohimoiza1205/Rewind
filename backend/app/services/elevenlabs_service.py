import requests
import logging
from typing import Optional
from app.config import settings
from app.services.cloudinary_service import cloudinary_service

logger = logging.getLogger(__name__)


def generate_narration(text: str, voice_id: Optional[str] = None) -> Optional[str]:
    """
    Generate voice narration using ElevenLabs API.
    
    Args:
        text: The caption/script to convert to speech
        voice_id: Optional voice ID (uses default if not provided)
    
    Returns:
        Audio file URL from Cloudinary (uploaded after generation)
    """
    try:
        if not voice_id:
            voice_id = settings.ELEVENLABS_DEFAULT_VOICE_ID
        
        logger.info(f"Generating narration for text: {text[:50]}...")
        
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": settings.ELEVENLABS_API_KEY
        }
        
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code != 200:
            raise Exception(f"ElevenLabs API error: {response.status_code}")
        
        audio_data = response.content
        logger.info(f"Generated audio: {len(audio_data)} bytes")
        
        audio_url = cloudinary_service.upload_audio(audio_data, f"narration_{voice_id}")
        
        logger.info(f"Uploaded to Cloudinary: {audio_url}")
        return audio_url
        
    except Exception as e:
        logger.error(f"Error generating narration: {str(e)}")
        return None


def clone_voice(audio_file_url: str, voice_name: str) -> Optional[str]:
    """
    Clone a voice from an audio sample (for custom user voices).
    
    Args:
        audio_file_url: URL of the audio sample
        voice_name: Name for the cloned voice
    
    Returns:
        voice_id of the cloned voice
    """
    try:
        logger.info(f"Cloning voice from: {audio_file_url}")
        
        audio_response = requests.get(audio_file_url)
        audio_data = audio_response.content
        
        url = "https://api.elevenlabs.io/v1/voices/add"
        
        headers = {
            "xi-api-key": settings.ELEVENLABS_API_KEY
        }
        
        files = {
            "files": ("sample.mp3", audio_data, "audio/mpeg")
        }
        
        data = {
            "name": voice_name,
            "description": f"Cloned voice for {voice_name}"
        }
        
        response = requests.post(url, headers=headers, files=files, data=data)
        
        if response.status_code != 200:
            raise Exception(f"Voice cloning error: {response.status_code}")
        
        result = response.json()
        voice_id = result.get("voice_id")
        
        logger.info(f"Voice cloned successfully: {voice_id}")
        return voice_id
        
    except Exception as e:
        logger.error(f"Error cloning voice: {str(e)}")
        return None