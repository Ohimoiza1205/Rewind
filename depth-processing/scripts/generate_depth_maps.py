import argparse
import sys
from pathlib import Path
import json
import cv2
from tqdm import tqdm
import logging

sys.path.append(str(Path(__file__).parent.parent / "src"))

from depth_estimator import DepthEstimator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_depth_maps(input_dir, output_dir, model_type="DPT_Large", 
                       save_visualization=True):
    """
    Generate high-quality depth maps for all frames
    
    Args:
        input_dir: Directory containing input RGB frames
        output_dir: Directory to save depth maps
        model_type: MiDaS model architecture
        save_visualization: Save colored depth visualizations
        
    Returns:
        Dictionary with processing metadata
    """
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    frame_files = sorted(input_dir.glob("*.jpg")) + sorted(input_dir.glob("*.png"))
    
    if not frame_files:
        logger.error(f"No image files found in {input_dir}")
        return None
    
    logger.info(f"Found {len(frame_files)} frames to process")
    logger.info(f"Using model: {model_type}")
    
    estimator = DepthEstimator(model_type=model_type)
    
    metadata = {
        "model_type": model_type,
        "total_frames": len(frame_files),
        "input_directory": str(input_dir),
        "output_directory": str(output_dir),
        "frames": []
    }
    
    if save_visualization:
        viz_dir = output_dir / "visualizations"
        viz_dir.mkdir(exist_ok=True)
    
    for i, frame_path in enumerate(tqdm(frame_files, desc="Generating depth maps")):
        try:
            depth = estimator.estimate_depth(frame_path, normalize=True)
            
            depth_output = output_dir / f"{frame_path.stem}_depth.png"
            cv2.imwrite(str(depth_output), depth)
            
            frame_metadata = {
                "index": i,
                "original_frame": frame_path.name,
                "depth_map": depth_output.name,
                "shape": depth.shape
            }
            
            if save_visualization:
                depth_colored = cv2.applyColorMap(depth, cv2.COLORMAP_INFERNO)
                viz_output = viz_dir / f"{frame_path.stem}_viz.png"
                cv2.imwrite(str(viz_output), depth_colored)
                frame_metadata["visualization"] = viz_output.name
            
            metadata["frames"].append(frame_metadata)
            
        except Exception as e:
            logger.error(f"Failed to process {frame_path.name}: {e}")
            continue
    
    metadata_path = output_dir / "depth_metadata.json"
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    logger.info(f"Generated {len(metadata['frames'])} depth maps")
    logger.info(f"Saved to: {output_dir}")
    logger.info(f"Metadata: {metadata_path}")
    
    return metadata


def create_depth_video(depth_dir, output_path, fps=2):
    """
    Create video from depth map visualizations
    
    Args:
        depth_dir: Directory containing depth visualizations
        output_path: Path to save output video
        fps: Frames per second
    """
    viz_dir = Path(depth_dir) / "visualizations"
    
    if not viz_dir.exists():
        logger.error(f"Visualization directory not found: {viz_dir}")
        return None
    
    viz_files = sorted(viz_dir.glob("*_viz.png"))
    
    if not viz_files:
        logger.error("No visualization files found")
        return None
    
    first_frame = cv2.imread(str(viz_files[0]))
    height, width = first_frame.shape[:2]
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
    
    for viz_file in tqdm(viz_files, desc="Creating depth video"):
        frame = cv2.imread(str(viz_file))
        out.write(frame)
    
    out.release()
    logger.info(f"Depth visualization video saved to: {output_path}")
    
    return output_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Generate depth maps from video frames using MiDaS'
    )
    parser.add_argument(
        'input_dir', 
        type=str, 
        help='Directory containing extracted frames'
    )
    parser.add_argument(
        '--output', 
        type=str, 
        default='output/depth_maps', 
        help='Output directory for depth maps'
    )
    parser.add_argument(
        '--model', 
        type=str, 
        default='DPT_Large',
        choices=['DPT_Large', 'DPT_Hybrid', 'MiDaS_small'],
        help='MiDaS model type (default: DPT_Large for best quality)'
    )
    parser.add_argument(
        '--no-viz', 
        action='store_true', 
        help='Skip colored visualizations'
    )
    parser.add_argument(
        '--create-video', 
        action='store_true', 
        help='Create video from depth visualizations'
    )
    
    args = parser.parse_args()
    
    metadata = generate_depth_maps(
        args.input_dir,
        args.output,
        model_type=args.model,
        save_visualization=not args.no_viz
    )
    
    if metadata and args.create_video:
        video_path = Path(args.output) / "depth_visualization.mp4"
        create_depth_video(args.output, video_path)
    
    logger.info(f"Next: python scripts/depth_to_pointcloud.py {args.output}")