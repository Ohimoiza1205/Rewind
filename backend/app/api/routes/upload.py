from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from app.services.cloudinary_service import cloudinary_service
from app.services.firebase_service import firebase_service
from app.services.video_processor import video_processor
from app.config import settings
from pathlib import Path
import uuid
import shutil
import logging
from typing import Dict
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


class VideoUploadResponse(BaseModel):
    video_id: str
    status: str
    message: str
    video_url: str
    metadata: Dict


class ProcessRequest(BaseModel):
    video_id: str


def process_video_background(video_id: str, video_path: str):
    """
    Background task to process video frames and audio
    """
    try:
        logger.info(f"Starting background processing for {video_id}")
        
        firebase_service.update_video_status(video_id, "processing_frames")
        frame_urls = video_processor.process_video_frames(video_path, video_id)
        
        firebase_service.update_video_status(video_id, "processing_audio")
        audio_url = video_processor.process_video_audio(video_path, video_id)
        
        firebase_service.update_video_status(video_id, "creating_thumbnail")
        thumbnail_url = video_processor.create_video_thumbnail(video_path, video_id)
        
        firebase_service.store_video_metadata(video_id, {
            "frame_count": len(frame_urls),
            "processing_complete": True
        })
        
        firebase_service.update_video_status(video_id, "frames_extracted")
        
        Path(video_path).unlink()
        
        logger.info(f"Background processing complete for {video_id}")
        
    except Exception as e:
        logger.error(f"Background processing failed for {video_id}: {e}")
        firebase_service.update_video_status(video_id, "processing_failed")
        
        if Path(video_path).exists():
            Path(video_path).unlink()


@router.post("/upload", response_model=VideoUploadResponse)
async def upload_video(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """
    Upload video file and start processing
    
    Endpoint: POST /api/upload
    
    Process:
    1. Validate video file
    2. Generate unique video_id
    3. Save video temporarily
    4. Upload to Cloudinary
    5. Extract metadata
    6. Store in Firebase
    7. Start background processing (frames + audio)
    
    Returns:
        VideoUploadResponse with video_id and status
    """
    
    if not file.content_type or not file.content_type.startswith('video/'):
        raise HTTPException(
            status_code=400,
            detail="File must be a video. Accepted formats: mp4, mov, avi, mkv"
        )
    
    file_size = 0
    chunk_size = 1024 * 1024
    temp_chunks = []
    
    while chunk := await file.read(chunk_size):
        file_size += len(chunk)
        temp_chunks.append(chunk)
        
        if file_size > settings.MAX_VIDEO_SIZE_MB * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail=f"Video file too large. Maximum size: {settings.MAX_VIDEO_SIZE_MB}MB"
            )
    
    video_id = str(uuid.uuid4())
    
    temp_dir = Path(settings.TEMP_DIR) / video_id
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    file_extension = Path(file.filename).suffix
    temp_video_path = temp_dir / f"original{file_extension}"
    
    try:
        with open(temp_video_path, 'wb') as buffer:
            for chunk in temp_chunks:
                buffer.write(chunk)
        
        logger.info(f"Video saved temporarily: {temp_video_path}")
        
        metadata = video_processor.get_video_info(str(temp_video_path))
        
        logger.info(f"Uploading video to Cloudinary: {video_id}")
        upload_result = cloudinary_service.upload_video(
            str(temp_video_path),
            video_id
        )
        
        video_data = {
            "video_id": video_id,
            "filename": file.filename,
            "file_size": file_size,
            "video_url": upload_result["url"],
            "public_id": upload_result["public_id"],
            "status": "uploaded",
            "width": metadata.get("width"),
            "height": metadata.get("height"),
            "duration": metadata.get("duration"),
            "fps": metadata.get("fps"),
            "codec": metadata.get("codec"),
            "total_frames": metadata.get("total_frames")
        }
        
        firebase_service.store_video_metadata(video_id, video_data)
        
        background_tasks.add_task(
            process_video_background,
            video_id,
            str(temp_video_path)
        )
        
        logger.info(f"Video upload complete: {video_id}")
        
        return VideoUploadResponse(
            video_id=video_id,
            status="uploaded",
            message="Video uploaded successfully. Processing frames in background.",
            video_url=upload_result["url"],
            metadata=metadata
        )
        
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        
        if temp_video_path.exists():
            temp_video_path.unlink()
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.get("/status/{video_id}")
async def get_video_status(video_id: str):
    """
    Get video processing status
    
    Endpoint: GET /api/status/{video_id}
    
    Returns:
        Current processing status and metadata
    """
    try:
        metadata = firebase_service.get_video_metadata(video_id)
        
        if not metadata:
            raise HTTPException(status_code=404, detail="Video not found")
        
        return {
            "video_id": video_id,
            "status": metadata.get("status", "unknown"),
            "frame_count": metadata.get("frame_count", 0),
            "video_url": metadata.get("video_url"),
            "thumbnail_url": metadata.get("thumbnail_url"),
            "audio_url": metadata.get("audio_url"),
            "processing_complete": metadata.get("processing_complete", False),
            "metadata": {
                "duration": metadata.get("duration"),
                "width": metadata.get("width"),
                "height": metadata.get("height"),
                "fps": metadata.get("fps")
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/process")
async def trigger_processing(request: ProcessRequest):
    """
    Manually trigger video processing
    
    Endpoint: POST /api/process
    
    Use this if automatic background processing failed
    """
    try:
        metadata = firebase_service.get_video_metadata(request.video_id)
        
        if not metadata:
            raise HTTPException(status_code=404, detail="Video not found")
        
        if metadata.get("status") == "processing_frames":
            raise HTTPException(
                status_code=400,
                detail="Video is already being processed"
            )
        
        video_url = metadata.get("video_url")
        
        return {
            "video_id": request.video_id,
            "status": "processing_queued",
            "message": "Processing has been queued"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to trigger processing: {e}")
        raise HTTPException(status_code=500, detail=str(e))