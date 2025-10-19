import logging

logger = logging.getLogger(__name__)

class MockElevenLabsService:
    """Mock ElevenLabs service for demo"""
    
    def __init__(self):
        logger.info("ElevenLabs mock mode initialized")
    
    async def clone_voice(self, audio_file: bytes, user_id: str):
        """Mock voice cloning"""
        return {
            "voice_id": f"voice_{user_id}_cloned",
            "status": "success"
        }
    
    async def text_to_speech(self, text: str, voice_id: str, language: str):
        """Mock TTS"""
        return b"mock_audio_data"

# Create instance
elevenlabs_service = MockElevenLabsService()
