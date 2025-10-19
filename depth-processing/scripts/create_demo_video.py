import cv2
import numpy as np
from pathlib import Path
import logging
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_side_by_side_video(frames_dir, depth_dir, output_path, fps=2):
    """
    Create side-by-side comparison video: original | depth | 3D visualization
    """
    frames_dir = Path(frames_dir)
    depth_dir = Path(depth_dir)
    
    frame_files = sorted(frames_dir.glob("frame_*.jpg"))
    depth_files = sorted(depth_dir.glob("*_depth.png"))
    viz_files = sorted((depth_dir / "visualizations").glob("*_viz.png"))
    
    if not frame_files or not depth_files:
        logger.error("Missing frames or depth maps")
        return
    
    first_frame = cv2.imread(str(frame_files[0]))
    h, w = first_frame.shape[:2]
    
    output_width = w * 3
    output_height = h
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(str(output_path), fourcc, fps, (output_width, output_height))
    
    logger.info(f"Creating demo video: {output_path}")
    
    for frame_file, depth_file, viz_file in tqdm(
        zip(frame_files, depth_files, viz_files),
        total=len(frame_files),
        desc="Creating demo video"
    ):
        frame = cv2.imread(str(frame_file))
        depth_gray = cv2.imread(str(depth_file), cv2.IMREAD_GRAYSCALE)
        depth_color = cv2.cvtColor(depth_gray, cv2.COLOR_GRAY2BGR)
        viz = cv2.imread(str(viz_file))
        
        combined = np.hstack([frame, depth_color, viz])
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(combined, 'Original', (10, 30), font, 1, (255, 255, 255), 2)
        cv2.putText(combined, 'Depth Map', (w + 10, 30), font, 1, (255, 255, 255), 2)
        cv2.putText(combined, 'Visualization', (w*2 + 10, 30), font, 1, (255, 255, 255), 2)
        
        out.write(combined)
    
    out.release()
    logger.info(f"Demo video saved: {output_path}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Create demo visualization video')
    parser.add_argument('frames_dir', type=str)
    parser.add_argument('depth_dir', type=str)
    parser.add_argument('--output', type=str, default='demo_depth_processing.mp4')
    parser.add_argument('--fps', type=int, default=2)
    
    args = parser.parse_args()
    
    create_side_by_side_video(args.frames_dir, args.depth_dir, args.output, args.fps)