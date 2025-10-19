import argparse
import sys
from pathlib import Path
import json
from tqdm import tqdm
import logging

sys.path.append(str(Path(__file__).parent.parent / "src"))

from pointcloud_generator import PointCloudGenerator, process_frame_to_pointcloud

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def batch_process_pointclouds(frames_dir, depth_dir, output_dir, 
                              focal_length=525.0, downsample=2, 
                              include_mesh=True):
    """
    Process all frame-depth pairs into point clouds
    
    Args:
        frames_dir: Directory containing original RGB frames
        depth_dir: Directory containing depth maps
        output_dir: Directory to save point clouds
        focal_length: Camera focal length
        downsample: Downsampling factor
        include_mesh: Whether to generate mesh data
        
    Returns:
        Metadata dictionary with all point cloud info
    """
    frames_dir = Path(frames_dir)
    depth_dir = Path(depth_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    frame_files = sorted(frames_dir.glob("frame_*.jpg"))
    depth_files = sorted(depth_dir.glob("*_depth.png"))
    
    if len(frame_files) != len(depth_files):
        logger.warning(
            f"Frame count mismatch: {len(frame_files)} frames, "
            f"{len(depth_files)} depth maps"
        )
    
    pairs = list(zip(frame_files, depth_files))
    
    if not pairs:
        logger.error("No frame-depth pairs found")
        return None
    
    logger.info(f"Processing {len(pairs)} frame-depth pairs")
    
    metadata = {
        "total_pointclouds": len(pairs),
        "focal_length": focal_length,
        "downsample_factor": downsample,
        "includes_mesh": include_mesh,
        "pointclouds": []
    }
    
    for i, (frame_path, depth_path) in enumerate(tqdm(pairs, desc="Generating point clouds")):
        try:
            pointcloud_data, json_path = process_frame_to_pointcloud(
                frame_path,
                depth_path,
                output_dir,
                focal_length=focal_length,
                downsample=downsample,
                include_mesh=include_mesh
            )
            
            metadata["pointclouds"].append({
                "index": i,
                "timestamp": i / 2.0,
                "frame": frame_path.name,
                "depth_map": depth_path.name,
                "pointcloud": json_path.name,
                "point_count": pointcloud_data['count'],
                "bounds": pointcloud_data['bounds']
            })
            
        except Exception as e:
            logger.error(f"Failed to process pair {i}: {e}")
            continue
    
    metadata_path = output_dir / "pointcloud_metadata.json"
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    logger.info(f"Generated {len(metadata['pointclouds'])} point clouds")
    logger.info(f"Saved to: {output_dir}")
    logger.info(f"Metadata: {metadata_path}")
    
    return metadata


def analyze_pointcloud_quality(metadata_path):
    """
    Analyze quality metrics of generated point clouds
    
    Args:
        metadata_path: Path to pointcloud metadata JSON
    """
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
    
    point_counts = [pc['point_count'] for pc in metadata['pointclouds']]
    
    logger.info("\nPoint Cloud Quality Analysis:")
    logger.info(f"  Total point clouds: {len(point_counts)}")
    logger.info(f"  Average points per cloud: {sum(point_counts) / len(point_counts):.0f}")
    logger.info(f"  Min points: {min(point_counts)}")
    logger.info(f"  Max points: {max(point_counts)}")
    logger.info(f"  Total points across all clouds: {sum(point_counts):,}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Convert depth maps to 3D point clouds for Three.js'
    )
    parser.add_argument(
        'frames_dir',
        type=str,
        help='Directory containing original RGB frames'
    )
    parser.add_argument(
        'depth_dir',
        type=str,
        help='Directory containing depth maps'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='output/pointclouds',
        help='Output directory for point clouds'
    )
    parser.add_argument(
        '--focal-length',
        type=float,
        default=525.0,
        help='Camera focal length in pixels'
    )
    parser.add_argument(
        '--downsample',
        type=int,
        default=2,
        help='Downsampling factor (1=no downsample, 2=half resolution)'
    )
    parser.add_argument(
        '--no-mesh',
        action='store_true',
        help='Skip mesh generation (points only)'
    )
    parser.add_argument(
        '--analyze',
        action='store_true',
        help='Analyze point cloud quality after generation'
    )
    
    args = parser.parse_args()
    
    metadata = batch_process_pointclouds(
        args.frames_dir,
        args.depth_dir,
        args.output,
        focal_length=args.focal_length,
        downsample=args.downsample,
        include_mesh=not args.no_mesh
    )
    
    if metadata and args.analyze:
        metadata_path = Path(args.output) / "pointcloud_metadata.json"
        analyze_pointcloud_quality(metadata_path)
    
    logger.info("\nPoint clouds ready for Three.js integration!")
    logger.info(f"Load JSON files from: {args.output}")