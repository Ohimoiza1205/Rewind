import numpy as np
import cv2
from pathlib import Path
import logging
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def apply_temporal_smoothing(depth_dir, output_dir, window_size=3):
    """
    Apply temporal smoothing across consecutive depth maps
    """
    depth_dir = Path(depth_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    depth_files = sorted(depth_dir.glob("*_depth.png"))
    
    if len(depth_files) < window_size:
        logger.warning("Not enough frames for temporal smoothing")
        return
    
    logger.info(f"Applying temporal smoothing with window size {window_size}")
    
    depth_maps = [cv2.imread(str(f), cv2.IMREAD_GRAYSCALE) for f in depth_files]
    
    smoothed_maps = []
    
    for i in tqdm(range(len(depth_maps)), desc="Smoothing frames"):
        start_idx = max(0, i - window_size // 2)
        end_idx = min(len(depth_maps), i + window_size // 2 + 1)
        
        window = depth_maps[start_idx:end_idx]
        averaged = np.mean(window, axis=0).astype(np.uint8)
        smoothed_maps.append(averaged)
        
        output_path = output_dir / f"{depth_files[i].stem}_smoothed.png"
        cv2.imwrite(str(output_path), averaged)
    
    logger.info(f"Smoothed {len(smoothed_maps)} depth maps saved to {output_dir}")
    return smoothed_maps


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Apply temporal smoothing to depth maps')
    parser.add_argument('depth_dir', type=str, help='Directory with depth maps')
    parser.add_argument('--output', type=str, default='output/depth_maps_smoothed')
    parser.add_argument('--window', type=int, default=3, help='Smoothing window size')
    
    args = parser.parse_args()
    
    apply_temporal_smoothing(args.depth_dir, args.output, args.window)