from app.utils.ffmpeg_helper import ffmpeg_helper
from app.services.cloudinary_service import cloudinary_service
from app.services.firebase_service import firebase_service
from app.config import settings
from pathlib import Path
from typing import List, Dict
import logging
import shutil

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VideoProcessor:
    """
    Production-grade video processing service
    Orchestrates frame extraction, audio extraction, and cloud uploads
    """
    
    def __init__(self):
        self.temp_dir = Path(settings.TEMP_DIR)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
    
    def process_video_frames(self, video_path: str, video_id: str) -> List[str]:
        """
        Extract frames from video and upload to Cloudinary
        
        Args:
            video_path: Path to video file
            video_id: Unique video identifier
            
        Returns:
            List of frame URLs
        """
        frames_dir = self.temp_dir / video_id / "frames"
        frames_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            logger.info(f"Extracting frames for video {video_id}")
            
            frame_paths = ffmpeg_helper.extract_frames(
                video_path,
                str(frames_dir),
                fps=settings.FRAMES_PER_SECOND
            )
            
            logger.info(f"Uploading {len(frame_paths)} frames to Cloudinary")
            
            frame_urls = []
            for index, frame_path in enumerate(frame_paths):
                result = cloudinary_service.upload_image(
                    frame_path,
                    video_id,
                    index
                )
                frame_urls.append(result["url"])
                
                if (index + 1) % 10 == 0:
                    logger.info(f"Uploaded {index + 1}/{len(frame_paths)} frames")
            
            firebase_service.store_frame_urls(video_id, frame_urls)
            
            shutil.rmtree(frames_dir)
            logger.info(f"Frame processing complete for {video_id}")
            
            return frame_urls
            
        except Exception as e:
            logger.error(f"Frame processing failed: {e}")
            if frames_dir.exists():
                shutil.rmtree(frames_dir)
            raise
    
    def process_video_audio(self, video_path: str, video_id: str) -> str:
        """
        Extract audio from video and upload to Cloudinary
        
        Args:
            video_path: Path to video file
            video_id: Unique video identifier
            
        Returns:
            Audio URL
        """
        audio_dir = self.temp_dir / video_id / "audio"
        audio_dir.mkdir(parents=True, exist_ok=True)
        
        audio_path = audio_dir / "original.mp3"
        
        try:
            logger.info(f"Extracting audio for video {video_id}")
            
            ffmpeg_helper.extract_audio(video_path, str(audio_path))
            
            logger.info(f"Uploading audio to Cloudinary")
            
            result = cloudinary_service.upload_audio(
                str(audio_path),
                video_id,
                "original"
            )
            
            audio_url = result["url"]
            
            firebase_service.store_video_metadata(video_id, {
                "audio_url": audio_url,
                "audio_duration": result.get("duration")
            })
            
            shutil.rmtree(audio_dir)
            logger.info(f"Audio processing complete for {video_id}")
            
            return audio_url
            
        except Exception as e:
            logger.error(f"Audio processing failed: {e}")
            if audio_dir.exists():
                shutil.rmtree(audio_dir)
            raise
    
    def get_video_info(self, video_path: str) -> Dict:
        """
        Extract video metadata
        
        Args:
            video_path: Path to video file
            
        Returns:
            Video metadata dictionary
        """
        try:
            metadata = ffmpeg_helper.get_video_metadata(video_path)
            return metadata
            
        except Exception as e:
            logger.error(f"Failed to get video info: {e}")
            raise
    
    def create_video_thumbnail(self, video_path: str, video_id: str) -> str:
        """
        Create and upload video thumbnail
        
        Args:
            video_path: Path to video file
            video_id: Unique video identifier
            
        Returns:
            Thumbnail URL
        """
        thumb_dir = self.temp_dir / video_id / "thumbnail"
        thumb_dir.mkdir(parents=True, exist_ok=True)
        
        thumb_path = thumb_dir / "thumbnail.jpg"
        
        try:
            logger.info(f"Creating thumbnail for video {video_id}")
            
            ffmpeg_helper.create_thumbnail(video_path, str(thumb_path), 1.0)
            
            result = cloudinary_service.upload_image(
                str(thumb_path),
                video_id,
                -1
            )
            
            thumbnail_url = result["url"]
            
            firebase_service.store_video_metadata(video_id, {
                "thumbnail_url": thumbnail_url
            })
            
            shutil.rmtree(thumb_dir)
            logger.info(f"Thumbnail created for {video_id}")
            
            return thumbnail_url
            
        except Exception as e:
            logger.error(f"Thumbnail creation failed: {e}")
            if thumb_dir.exists():
                shutil.rmtree(thumb_dir)
            raise
    
    def cleanup_temp_files(self, video_id: str):
        """
        Clean up temporary files for a video
        
        Args:
            video_id: Video identifier
        """
        video_temp_dir = self.temp_dir / video_id
        
        if video_temp_dir.exists():
            shutil.rmtree(video_temp_dir)
            logger.info(f"Cleaned up temp files for {video_id}")


video_processor = VideoProcessor()