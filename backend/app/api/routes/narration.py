from fastapi import APIRouter, HTTPException
from app.services import elevenlabs_service
from app.services import cloudinary_service
from pydantic import BaseModel
import uuid

router = APIRouter()

class NarrationRequest(BaseModel):
    text: str
    voice_id: str = None
    video_id: str

@router.post("/narrate")
async def create_narration(request: NarrationRequest):
    try:
        # Generate audio
        audio_bytes = elevenlabs_service.text_to_speech(
            request.text,
            request.voice_id
        )
        
        # Save temporarily
        audio_filename = f"{request.video_id}_{uuid.uuid4()}.mp3"
        audio_path = elevenlabs_service.save_audio_file(audio_bytes, audio_filename)
        
        # Upload to Cloudinary
        upload_result = cloudinary_service.upload_audio(
            audio_path,
            folder=f"rewind/narration/{request.video_id}"
        )
        
        return {
            "video_id": request.video_id,
            "text": request.text,
            "audio_url": upload_result["url"],
            "public_id": upload_result["public_id"],
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/voices")
async def list_voices():
    try:
        voices = elevenlabs_service.get_available_voices()
        return voices
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
