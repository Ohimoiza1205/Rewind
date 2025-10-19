from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
import logging
import json

router = APIRouter()
logger = logging.getLogger(__name__)

POINTCLOUD_BASE = Path(__file__).parent.parent.parent.parent.parent / "depth-processing" / "output"

@router.get("/pointcloud/videos")
async def list_videos():
    """List all videos with point clouds"""
    try:
        pointcloud_dir = POINTCLOUD_BASE / "pointclouds"
        
        if not pointcloud_dir.exists():
            return {"success": True, "videos": []}
        
        videos = [d.name for d in pointcloud_dir.iterdir() if d.is_dir()]
        
        return {
            "success": True,
            "videos": videos,
            "total": len(videos)
        }
    except Exception as e:
        logger.error(f"Error listing videos: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/pointcloud/metadata/{video_name}")
async def get_metadata(video_name: str):
    """Get pipeline metadata for a video"""
    try:
        metadata_path = POINTCLOUD_BASE / "pointclouds" / video_name / "pipeline_metadata.json"
        
        if not metadata_path.exists():
            raise HTTPException(status_code=404, detail="Metadata not found")
        
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        return {"success": True, "metadata": metadata}
    except Exception as e:
        logger.error(f"Error getting metadata: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/pointcloud/frame/{video_name}/{frame_number}")
async def get_frame(video_name: str, frame_number: int):
    """Get specific point cloud frame JSON"""
    try:
        frame_file = POINTCLOUD_BASE / "pointclouds" / video_name / f"frame_{frame_number:04d}.json"
        
        if not frame_file.exists():
            raise HTTPException(status_code=404, detail="Frame not found")
        
        return FileResponse(
            path=str(frame_file),
            media_type="application/json"
        )
    except Exception as e:
        logger.error(f"Error getting frame: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/pointcloud/frames/{video_name}")
async def get_frame_image(video_name: str, frame_number: int):
    """Get original frame image"""
    try:
        frame_file = POINTCLOUD_BASE / "frames" / video_name / f"frame_{frame_number:04d}.jpg"
        
        if not frame_file.exists():
            raise HTTPException(status_code=404, detail="Frame image not found")
        
        return FileResponse(
            path=str(frame_file),
            media_type="image/jpeg"
        )
    except Exception as e:
        logger.error(f"Error getting frame image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))