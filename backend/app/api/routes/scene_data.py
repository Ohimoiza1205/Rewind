from fastapi import APIRouter

router = APIRouter()

@router.get("/scenes/{video_id}")
async def get_scenes(video_id: str):
    return {"message": "Gemini scene data endpoint - coming soon"}
