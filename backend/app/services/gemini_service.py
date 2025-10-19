import logging

logger = logging.getLogger(__name__)

class MockGeminiService:
    """Mock Gemini service for demo"""
    
    def __init__(self):
        logger.info("Gemini mock mode initialized")
    
    async def describe_scenes(self, scene_data):
        """Mock scene descriptions"""
        return [
            "Here's Emma blowing out the candles on her fifth birthday cake surrounded by family and friends celebrating this special moment.",
            "The excitement fills the room as everyone gathers around to sing Happy Birthday while the candles glow brightly."
        ]
    
    async def translate_text(self, text: str, target_language: str):
        """Mock translation"""
        translations = {
            "es": "Aquí está Emma soplando las velas de su pastel de quinto cumpleaños rodeada de familia y amigos celebrando este momento especial.",
            "fr": "Voici Emma soufflant les bougies de son gâteau d'anniversaire entourée de sa famille et de ses amis célébrant ce moment spécial.",
            "de": "Hier bläst Emma die Kerzen auf ihrer Geburtstagstorte aus, umgeben von Familie und Freunden, die diesen besonderen Moment feiern."
        }
        return translations.get(target_language, text)

# Create instance
gemini_service = MockGeminiService()
