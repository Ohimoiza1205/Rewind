import cloudinary
import cloudinary.uploader
from app.config import settings
from pathlib import Path
import logging
from typing import Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CloudinaryService:
    """
    Production-grade Cloudinary file storage service
    Handles uploads for videos, images, JSON, and audio files
    """
    
    def __init__(self):
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET,
            secure=True
        )
        logger.info("Cloudinary configured successfully")
    
    def upload_video(self, file_path: str, video_id: str) -> Dict[str, str]:
        """
        Upload video file to Cloudinary
        
        Args:
            file_path: Local path to video file
            video_id: Unique identifier for video
            
        Returns:
            Dictionary with url and public_id
        """
        try:
            result = cloudinary.uploader.upload(
                file_path,
                resource_type="video",
                folder=f"rewind/videos/{video_id}",
                overwrite=True,
                invalidate=True
            )
            
            logger.info(f"Video uploaded: {result['public_id']}")
            
            return {
                "url": result['secure_url'],
                "public_id": result['public_id'],
                "format": result['format'],
                "duration": result.get('duration'),
                "width": result.get('width'),
                "height": result.get('height')
            }
            
        except Exception as e:
            logger.error(f"Video upload failed: {e}")
            raise
    
    def upload_image(self, file_path: str, video_id: str, frame_index: int) -> Dict[str, str]:
        """
        Upload image frame to Cloudinary
        
        Args:
            file_path: Local path to image file
            video_id: Video identifier
            frame_index: Frame number
            
        Returns:
            Dictionary with url and public_id
        """
        try:
            result = cloudinary.uploader.upload(
                file_path,
                resource_type="image",
                folder=f"rewind/videos/{video_id}/frames",
                public_id=f"frame_{frame_index:04d}",
                overwrite=True,
                invalidate=True
            )
            
            return {
                "url": result['secure_url'],
                "public_id": result['public_id'],
                "width": result['width'],
                "height": result['height']
            }
            
        except Exception as e:
            logger.error(f"Image upload failed for frame {frame_index}: {e}")
            raise
    
    def upload_json(self, file_path: str, video_id: str, frame_index: int) -> Dict[str, str]:
        """
        Upload point cloud JSON to Cloudinary
        
        Args:
            file_path: Local path to JSON file
            video_id: Video identifier
            frame_index: Frame number
            
        Returns:
            Dictionary with url and public_id
        """
        try:
            result = cloudinary.uploader.upload(
                file_path,
                resource_type="raw",
                folder=f"rewind/videos/{video_id}/pointclouds",
                public_id=f"frame_{frame_index:04d}",
                overwrite=True,
                invalidate=True
            )
            
            return {
                "url": result['secure_url'],
                "public_id": result['public_id'],
                "bytes": result['bytes']
            }
            
        except Exception as e:
            logger.error(f"JSON upload failed for frame {frame_index}: {e}")
            raise
    
    def upload_audio(self, file_path: str, video_id: str, audio_type: str = "narration") -> Dict[str, str]:
        """
        Upload audio file to Cloudinary
        
        Args:
            file_path: Local path to audio file
            video_id: Video identifier
            audio_type: Type of audio (narration, original, etc.)
            
        Returns:
            Dictionary with url and public_id
        """
        try:
            result = cloudinary.uploader.upload(
                file_path,
                resource_type="video",
                folder=f"rewind/videos/{video_id}/audio",
                public_id=audio_type,
                overwrite=True,
                invalidate=True
            )
            
            return {
                "url": result['secure_url'],
                "public_id": result['public_id'],
                "format": result['format'],
                "duration": result.get('duration')
            }
            
        except Exception as e:
            logger.error(f"Audio upload failed: {e}")
            raise
    
    def delete_resource(self, public_id: str, resource_type: str = "image") -> bool:
        """
        Delete resource from Cloudinary
        
        Args:
            public_id: Cloudinary public ID
            resource_type: Type of resource (image, video, raw)
            
        Returns:
            True if successful
        """
        try:
            cloudinary.uploader.destroy(public_id, resource_type=resource_type)
            logger.info(f"Deleted resource: {public_id}")
            return True
            
        except Exception as e:
            logger.error(f"Delete failed: {e}")
            return False


cloudinary_service = CloudinaryService()