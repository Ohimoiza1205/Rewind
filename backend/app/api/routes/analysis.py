from fastapi import APIRouter

router = APIRouter()

@router.post("/analyze")
async def analyze_video():
    return {"message": "TwelveLabs analysis endpoint - coming soon"}

