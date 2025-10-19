import requests
from app.config import settings

# Try gemini-1.5-flash-latest
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

def generate_scene_description(scene_data: dict) -> str:
    """Generate natural language description for a video scene"""
    
    prompt = f"""
    Based on this video scene data, create a natural, conversational description:
    
    Timestamp: {scene_data.get('timestamp', 'Unknown')}
    Objects detected: {', '.join(scene_data.get('objects', []))}
    People: {', '.join(scene_data.get('people', []))}
    Audio/Speech: {scene_data.get('transcript', 'No speech detected')}
    
    Create a single sentence description like "This is [person] doing [action] during [context]"
    Keep it natural and conversational.
    """
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }
    
    response = requests.post(
        f"{GEMINI_API_URL}?key={settings.GEMINI_API_KEY}",
        headers=headers,
        json=payload
    )
    
    if response.status_code == 200:
        result = response.json()
        return result['candidates'][0]['content']['parts'][0]['text']
    else:
        raise Exception(f"Gemini API error: {response.status_code} - {response.text}")

def generate_object_caption(object_name: str, context: dict) -> str:
    """Generate caption for a specific object in the scene"""
    
    prompt = f"""
    Create a brief caption (1 sentence) for this object in a video:
    
    Object: {object_name}
    Scene context: {context.get('description', 'A video scene')}
    Timestamp: {context.get('timestamp', 'Unknown')}
    
    Make it natural and interesting, like you're explaining it to a friend.
    """
    
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    response = requests.post(
        f"{GEMINI_API_URL}?key={settings.GEMINI_API_KEY}",
        headers=headers,
        json=payload
    )
    
    if response.status_code == 200:
        result = response.json()
        return result['candidates'][0]['content']['parts'][0]['text']
    else:
        raise Exception(f"Gemini API error: {response.status_code} - {response.text}")

def answer_scene_question(scene_data: dict, question: str) -> str:
    """Answer questions about what's happening in a scene"""
    
    prompt = f"""
    Based on this video scene data:
    
    Objects: {scene_data.get('objects', [])}
    People: {scene_data.get('people', [])}
    Transcript: {scene_data.get('transcript', 'None')}
    Timestamp: {scene_data.get('timestamp', 'Unknown')}
    
    Question: {question}
    
    Provide a clear, concise answer.
    """
    
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    response = requests.post(
        f"{GEMINI_API_URL}?key={settings.GEMINI_API_KEY}",
        headers=headers,
        json=payload
    )
    
    if response.status_code == 200:
        result = response.json()
        return result['candidates'][0]['content']['parts'][0]['text']
    else:
        raise Exception(f"Gemini API error: {response.status_code} - {response.text}")
