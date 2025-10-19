from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from app.config import settings
from app.services.depth_processing_service import process_video_depth
from app.services.ai_pipeline_service import process_video_ai
import logging
import os
import shutil
from pathlib import Path

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/upload")
async def upload_video(file: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    try:
        logger.info(f"Received upload request for file: {file.filename}")
        
        if not file.content_type.startswith('video/'):
            raise HTTPException(status_code=400, detail="File must be a video")
        
        temp_dir = Path(settings.TEMP_DIR)
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        temp_file_path = temp_dir / file.filename
        
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        file_size_mb = temp_file_path.stat().st_size / (1024 * 1024)
        logger.info(f"File saved temporarily: {file_size_mb:.2f} MB")
        
        video_id = f"video_{os.urandom(8).hex()}"
        
        background_tasks.add_task(process_video_depth, str(temp_file_path), video_id)
        background_tasks.add_task(process_video_ai, video_id, str(temp_file_path))
        
        return {
            "video_id": video_id,
            "url": f"/temp/{file.filename}",
            "status": "uploaded",
            "message": "Video uploaded successfully. Processing started.",
            "file_size_mb": round(file_size_mb, 2)
        }
        
    except Exception as e:
        logger.error(f"Upload failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.get("/status/{video_id}")
async def get_video_status(video_id: str):
    return {
        "video_id": video_id,
        "status": "processing",
        "progress": 50
    }

@router.post("/process")
async def trigger_processing(video_id: str):
    return {
        "video_id": video_id,
        "status": "processing_started"
    }
@router.get("/depth-status/{video_id}")
async def get_depth_status(video_id: str):
    from app.services.depth_processing_service import get_processing_status
    status = get_processing_status(video_id)
    return {
        "video_id": video_id,
        "depth_processing": status
    }
@router.get("/ai-results/{video_id}")
async def get_ai_results(video_id: str):
    from app.services.firebase_service import firebase_service
    
    results = firebase_service.get_video_analysis(video_id)
    
    if not results:
        return {
            "video_id": video_id,
            "status": "processing",
            "scenes": []
        }
    
    return {
        "video_id": video_id,
        "status": "complete",
        "scenes": results.get("scenes", [])
    }