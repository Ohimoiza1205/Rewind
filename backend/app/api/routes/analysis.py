from fastapi import APIRouter, HTTPException
from app.services import twelvelabs_service
from app.services import firebase_service
from pydantic import BaseModel

router = APIRouter()

INDEX_ID = "68f4397213449bce9693b5bf"

class AnalyzeRequest(BaseModel):
    video_url: str
    video_id: str

@router.post("/analyze")
async def analyze_video(request: AnalyzeRequest):
    try:
        task = twelvelabs_service.upload_video_to_twelvelabs(
            request.video_url,
            INDEX_ID
        )
        
        firebase_service.store_video_metadata(request.video_id, {
            "twelvelabs_task_id": task.id,
            "twelvelabs_index_id": INDEX_ID,
            "video_url": request.video_url,
            "status": "processing"
        })
        
        return {
            "video_id": request.video_id,
            "task_id": task.id,
            "index_id": INDEX_ID,
            "status": "processing",
            "message": "Video sent to TwelveLabs for analysis"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analyze/{video_id}/status")
async def get_analysis_status(video_id: str):
    try:
        metadata = firebase_service.get_video_metadata(video_id)
        
        if not metadata:
            raise HTTPException(status_code=404, detail="Video not found")
        
        task_id = metadata.get("twelvelabs_task_id")
        status = twelvelabs_service.get_task_status(task_id)
        
        return {
            "video_id": video_id,
            "status": status,
            "task_id": task_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
