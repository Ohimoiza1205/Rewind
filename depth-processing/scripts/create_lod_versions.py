import json
from pathlib import Path
import numpy as np
import logging
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_lod_versions(pointcloud_dir, output_dir):
    """
    Create Level of Detail (LOD) versions for performance
    """
    pointcloud_dir = Path(pointcloud_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    lod_levels = {
        'high': 1.0,
        'medium': 0.5,
        'low': 0.25
    }
    
    json_files = sorted(pointcloud_dir.glob("frame_*.json"))
    
    for json_file in tqdm(json_files, desc="Creating LOD versions"):
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        points = np.array(data['points'])
        colors = np.array(data['colors'])
        
        for lod_name, ratio in lod_levels.items():
            lod_dir = output_dir / lod_name
            lod_dir.mkdir(exist_ok=True)
            
            num_points = int(len(points) * ratio)
            indices = np.random.choice(len(points), num_points, replace=False)
            
            lod_data = {
                'type': data['type'],
                'points': points[indices].tolist(),
                'colors': colors[indices].tolist(),
                'metadata': {
                    'count': num_points,
                    'lod_level': lod_name,
                    'original_count': data['metadata']['count']
                }
            }
            
            output_path = lod_dir / json_file.name
            with open(output_path, 'w') as f:
                json.dump(lod_data, f, separators=(',', ':'))
    
    logger.info(f"LOD versions created in {output_dir}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Create LOD versions')
    parser.add_argument('pointcloud_dir', type=str)
    parser.add_argument('--output', type=str, default='output/pointclouds_lod')
    
    args = parser.parse_args()
    
    create_lod_versions(args.pointcloud_dir, args.output)