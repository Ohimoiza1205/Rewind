import subprocess
import json
from pathlib import Path
from typing import List, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FFmpegHelper:
    """
    Production-grade FFmpeg utilities for video processing
    Handles frame extraction, audio extraction, and metadata retrieval
    """
    
    @staticmethod
    def extract_frames(video_path: str, output_dir: str, fps: int = 2) -> List[str]:
        """
        Extract frames from video at specified fps
        
        Args:
            video_path: Path to input video
            output_dir: Directory to save frames
            fps: Frames per second to extract
            
        Returns:
            List of frame file paths
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_pattern = output_dir / "frame_%04d.jpg"
        
        command = [
            'ffmpeg',
            '-i', str(video_path),
            '-vf', f'fps={fps}',
            '-q:v', '2',
            '-start_number', '0',
            str(output_pattern),
            '-y'
        ]
        
        try:
            result = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True
            )
            
            frame_files = sorted(output_dir.glob("frame_*.jpg"))
            logger.info(f"Extracted {len(frame_files)} frames from {video_path}")
            
            return [str(f) for f in frame_files]
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Frame extraction failed: {e.stderr}")
            raise RuntimeError(f"FFmpeg frame extraction failed: {e.stderr}")
    
    @staticmethod
    def extract_audio(video_path: str, output_path: str) -> str:
        """
        Extract audio track from video
        
        Args:
            video_path: Path to input video
            output_path: Path to save audio file
            
        Returns:
            Path to extracted audio file
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        command = [
            'ffmpeg',
            '-i', str(video_path),
            '-vn',
            '-acodec', 'libmp3lame',
            '-q:a', '0',
            str(output_path),
            '-y'
        ]
        
        try:
            subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True
            )
            
            logger.info(f"Extracted audio to {output_path}")
            return str(output_path)
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Audio extraction failed: {e.stderr}")
            raise RuntimeError(f"FFmpeg audio extraction failed: {e.stderr}")
    
    @staticmethod
    def get_video_metadata(video_path: str) -> Dict:
        """
        Extract comprehensive video metadata using FFprobe
        
        Args:
            video_path: Path to video file
            
        Returns:
            Dictionary with video metadata
        """
        command = [
            'ffprobe',
            '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries',
            'stream=width,height,r_frame_rate,duration,nb_frames,codec_name',
            '-of', 'json',
            str(video_path)
        ]
        
        try:
            result = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True
            )
            
            data = json.loads(result.stdout)
            stream = data['streams'][0]
            
            fps_str = stream['r_frame_rate']
            fps_num, fps_den = map(int, fps_str.split('/'))
            fps = fps_num / fps_den
            
            metadata = {
                'width': stream['width'],
                'height': stream['height'],
                'fps': round(fps, 2),
                'duration': float(stream.get('duration', 0)),
                'total_frames': int(stream.get('nb_frames', 0)),
                'codec': stream['codec_name']
            }
            
            logger.info(f"Video metadata: {metadata}")
            return metadata
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Metadata extraction failed: {e.stderr}")
            raise RuntimeError(f"FFprobe failed: {e.stderr}")
        except (KeyError, json.JSONDecodeError) as e:
            logger.error(f"Failed to parse metadata: {e}")
            raise RuntimeError(f"Invalid metadata format: {e}")
    
    @staticmethod
    def get_video_duration(video_path: str) -> float:
        """
        Get video duration in seconds
        
        Args:
            video_path: Path to video file
            
        Returns:
            Duration in seconds
        """
        command = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            str(video_path)
        ]
        
        try:
            result = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True
            )
            
            duration = float(result.stdout.strip())
            return duration
            
        except (subprocess.CalledProcessError, ValueError) as e:
            logger.error(f"Duration extraction failed: {e}")
            return 0.0
    
    @staticmethod
    def create_thumbnail(video_path: str, output_path: str, timestamp: float = 1.0) -> str:
        """
        Extract thumbnail from video at specific timestamp
        
        Args:
            video_path: Path to video file
            output_path: Path to save thumbnail
            timestamp: Time in seconds to extract frame
            
        Returns:
            Path to thumbnail
        """
        command = [
            'ffmpeg',
            '-i', str(video_path),
            '-ss', str(timestamp),
            '-vframes', '1',
            '-q:v', '2',
            str(output_path),
            '-y'
        ]
        
        try:
            subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True
            )
            
            logger.info(f"Created thumbnail at {output_path}")
            return str(output_path)
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Thumbnail creation failed: {e.stderr}")
            raise RuntimeError(f"FFmpeg thumbnail failed: {e.stderr}")


ffmpeg_helper = FFmpegHelper()