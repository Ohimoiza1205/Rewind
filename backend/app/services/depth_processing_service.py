import subprocess
import logging
from pathlib import Path
from typing import Optional
import threading
import time

logger = logging.getLogger(__name__)

DEPTH_PROCESSING_DIR = Path(__file__).parent.parent.parent.parent / "depth-processing"

processing_status = {}


def run_depth_processing(video_path: str, video_id: str):
    """Run depth processing and log output in real-time"""
    try:
        processing_status[video_id] = {"status": "running", "progress": 0}
        
        logger.info(f"Starting depth processing thread for video: {video_id}")
        
        script_path = DEPTH_PROCESSING_DIR / "scripts" / "batch_process.py"
        output_dir = DEPTH_PROCESSING_DIR / "output"
        
        cmd = [
            "python",
            str(script_path),
            video_path,
            "--fps", "2",
            "--model", "DPT_Large",
            "--downsample", "2",
            "--output", str(output_dir)
        ]
        
        logger.info(f"Running command: {' '.join(cmd)}")
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        for line in process.stdout:
            logger.info(f"[{video_id}] {line.strip()}")
            
            if "Processing point cloud" in line:
                parts = line.split("/")
                if len(parts) >= 2:
                    current = int(parts[0].split()[-1])
                    total = int(parts[1].split()[0])
                    progress = int((current / total) * 100)
                    processing_status[video_id]["progress"] = progress
        
        process.wait()
        
        if process.returncode == 0:
            processing_status[video_id] = {"status": "complete", "progress": 100}
            logger.info(f"Depth processing complete for {video_id}")
        else:
            processing_status[video_id] = {"status": "failed", "progress": 0}
            logger.error(f"Depth processing failed for {video_id}")
            
    except Exception as e:
        processing_status[video_id] = {"status": "error", "progress": 0}
        logger.error(f"Error in depth processing: {str(e)}")


def process_video_depth(video_path: str, video_id: str) -> Optional[dict]:
    """Trigger depth processing pipeline in background thread"""
    try:
        thread = threading.Thread(
            target=run_depth_processing,
            args=(video_path, video_id),
            daemon=True
        )
        thread.start()
        
        logger.info(f"Depth processing started in background for {video_id}")
        
        return {
            "status": "started",
            "video_id": video_id
        }
        
    except Exception as e:
        logger.error(f"Error starting depth processing: {str(e)}")
        return None


def get_processing_status(video_id: str) -> dict:
    """Get current processing status for a video"""
    return processing_status.get(video_id, {"status": "not_found", "progress": 0})