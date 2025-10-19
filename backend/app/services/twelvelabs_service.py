import logging

logger = logging.getLogger(__name__)

class MockTwelveLabsService:
    """Mock TwelveLabs service for demo"""
    
    def __init__(self):
        logger.info("TwelveLabs mock mode initialized")
    
    async def analyze_video(self, video_url: str):
        """Mock video analysis"""
        return {
            "scenes": [
                {
                    "start_time": 0,
                    "end_time": 5,
                    "description": "People celebrating at a birthday party",
                    "objects": ["cake", "candles", "balloons", "people"]
                },
                {
                    "start_time": 5,
                    "end_time": 10,
                    "description": "Child blowing out birthday candles",
                    "objects": ["child", "cake", "candles", "celebration"]
                }
            ]
        }

# Create instance
twelvelabs_service = MockTwelveLabsService()
