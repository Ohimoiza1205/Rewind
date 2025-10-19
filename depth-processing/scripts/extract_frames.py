import subprocess
import argparse
from pathlib import Path
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def extract_frames(video_path, output_dir, fps=2, quality=2):
    """
    Extract high-quality frames from video using FFmpeg
    
    Args:
        video_path: Path to input video file
        output_dir: Directory to save extracted frames
        fps: Frames per second to extract
        quality: JPEG quality (1-31, lower is better, 2 is very high)
        
    Returns:
        List of extracted frame paths
    """
    video_path = Path(video_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if not video_path.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")
    
    output_pattern = output_dir / "frame_%04d.jpg"
    
    command = [
        'ffmpeg',
        '-i', str(video_path),
        '-vf', f'fps={fps}',
        '-q:v', str(quality),
        '-start_number', '0',
        str(output_pattern)
    ]
    
    logger.info(f"Extracting frames from: {video_path.name}")
    logger.info(f"Output directory: {output_dir}")
    logger.info(f"Target FPS: {fps}")
    
    try:
        result = subprocess.run(
            command, 
            check=True, 
            capture_output=True, 
            text=True
        )
        
        frame_files = sorted(output_dir.glob("frame_*.jpg"))
        logger.info(f"Successfully extracted {len(frame_files)} frames")
        
        return frame_files
        
    except subprocess.CalledProcessError as e:
        logger.error(f"FFmpeg error: {e.stderr}")
        raise
    except FileNotFoundError:
        logger.error("FFmpeg not found. Please install FFmpeg.")
        raise


def extract_audio(video_path, output_path):
    """
    Extract audio track from video in high quality
    
    Args:
        video_path: Path to input video
        output_path: Path to save audio file (MP3)
        
    Returns:
        Path to extracted audio file
    """
    video_path = Path(video_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    command = [
        'ffmpeg',
        '-i', str(video_path),
        '-vn',
        '-acodec', 'libmp3lame',
        '-q:a', '0',
        '-y',
        str(output_path)
    ]
    
    logger.info(f"Extracting audio from: {video_path.name}")
    
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        logger.info(f"Audio extracted to: {output_path}")
        return output_path
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Audio extraction failed: {e.stderr}")
        return None


def get_video_metadata(video_path):
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
            capture_output=True, 
            text=True, 
            check=True
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
        
    except Exception as e:
        logger.error(f"Failed to get video metadata: {e}")
        return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Extract frames and audio from video files'
    )
    parser.add_argument(
        'video', 
        type=str, 
        help='Path to input video file'
    )
    parser.add_argument(
        '--fps', 
        type=int, 
        default=2, 
        help='Frames per second to extract (default: 2)'
    )
    parser.add_argument(
        '--output', 
        type=str, 
        default='output/frames', 
        help='Output directory for frames'
    )
    parser.add_argument(
        '--audio', 
        action='store_true', 
        help='Also extract audio track'
    )
    parser.add_argument(
        '--quality', 
        type=int, 
        default=2, 
        help='JPEG quality (1-31, lower is better)'
    )
    
    args = parser.parse_args()
    
    video_path = Path(args.video)
    
    if not video_path.exists():
        logger.error(f"Video file not found: {video_path}")
        exit(1)
    
    metadata = get_video_metadata(video_path)
    
    frames = extract_frames(
        video_path, 
        args.output, 
        fps=args.fps, 
        quality=args.quality
    )
    
    if args.audio:
        audio_dir = Path(args.output).parent / "audio"
        audio_path = audio_dir / f"{video_path.stem}.mp3"
        extract_audio(video_path, audio_path)
    
    metadata_path = Path(args.output) / "metadata.json"
    if metadata:
        metadata['extracted_frames'] = len(frames)
        metadata['extraction_fps'] = args.fps
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    logger.info("Frame extraction complete")
    logger.info(f"Next: python scripts/generate_depth_maps.py {args.output}")