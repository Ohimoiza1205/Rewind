from fastapi import APIRouter, UploadFile, File, HTTPException
from app.config import settings
import logging
import os
import shutil
from pathlib import Path

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    try:
        logger.info(f"Received upload request for file: {file.filename}")
        
        # Validate file type
        if not file.content_type.startswith('video/'):
            raise HTTPException(status_code=400, detail="File must be a video")
        
        # Create temp directory if it doesn't exist
        temp_dir = Path(settings.TEMP_DIR)
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        # Save to temporary file
        temp_file_path = temp_dir / file.filename
        
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        file_size_mb = temp_file_path.stat().st_size / (1024 * 1024)
        logger.info(f"File saved temporarily: {file_size_mb:.2f} MB")
        
        # For now, just return success (we'll integrate Cloudinary properly later)
        video_id = f"video_{os.urandom(8).hex()}"
        
        return {
            "video_id": video_id,
            "url": f"/temp/{file.filename}",
            "status": "uploaded",
            "message": "Video uploaded successfully",
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
