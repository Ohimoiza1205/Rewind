from fastapi import APIRouter

router = APIRouter()

@router.post("/narrate")
async def create_narration():
    return {"message": "ElevenLabs narration endpoint - coming soon"}

