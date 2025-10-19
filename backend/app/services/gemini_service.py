import requests
import logging
from typing import Dict
from app.config import settings

logger = logging.getLogger(__name__)


def generate_scene_description(scene_data: Dict) -> str:
    """
    Generate natural language description of a video scene using Gemini.
    
    Args:
        scene_data: Dictionary containing scene information
            - timestamp: Scene timestamp
            - objects: List of detected objects
            - people: List of detected people
            - transcript: Audio transcript
    
    Returns:
        Natural language description of the scene
    """
    try:
        timestamp = scene_data.get("timestamp", "unknown")
        objects = scene_data.get("objects", [])
        people = scene_data.get("people", [])
        transcript = scene_data.get("transcript", "")
        
        prompt = f"""Generate a natural, engaging description of this video scene.

Scene Details:
- Timestamp: {timestamp}
- Objects visible: {', '.join(objects) if objects else 'none detected'}
- People: {', '.join(people) if people else 'none detected'}
- Audio transcript: "{transcript if transcript else 'no audio'}"

Create a brief, vivid description (2-3 sentences) that captures what's happening in this moment.
Focus on the action, emotion, and context. Write in present tense."""

        url = f"{settings.GEMINI_BASE_URL}/models/gemini-2.5-flash:generateContent?key={settings.GEMINI_API_KEY}"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        data = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }]
        }
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code != 200:
            raise Exception(f"Gemini API error: {response.status_code}")
        
        result = response.json()
        description = result["candidates"][0]["content"]["parts"][0]["text"]
        
        logger.info(f"Generated description for scene at {timestamp}")
        return description.strip()
        
    except Exception as e:
        logger.error(f"Error generating scene description: {str(e)}")
        return f"Scene at {scene_data.get('timestamp', 'unknown')}: Unable to generate description"