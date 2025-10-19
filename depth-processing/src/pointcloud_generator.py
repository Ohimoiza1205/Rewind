import numpy as np
import cv2
from pathlib import Path
import json
from scipy.spatial import Delaunay
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PointCloudGenerator:
    """
    High-quality point cloud generation optimized for Three.js
    Creates dense, accurate 3D representations from depth maps
    """
    
    def __init__(self, focal_length=525.0, max_depth=10.0):
        """
        Initialize point cloud generator
        
        Args:
            focal_length: Camera focal length in pixels
            max_depth: Maximum depth value in meters
        """
        self.focal_length = focal_length
        self.max_depth = max_depth
    
    def depth_to_pointcloud(self, depth_map, rgb_image, downsample_factor=1):
        """
        Convert depth map and RGB image to 3D point cloud
        
        Args:
            depth_map: Depth map (grayscale, 0-255)
            rgb_image: RGB image (same dimensions as depth)
            downsample_factor: Factor to reduce point count (1 = no downsampling)
            
        Returns:
            Dictionary with points, colors, and metadata
        """
        height, width = depth_map.shape
        
        if downsample_factor > 1:
            depth_map = depth_map[::downsample_factor, ::downsample_factor]
            rgb_image = rgb_image[::downsample_factor, ::downsample_factor]
            height, width = depth_map.shape
        
        depth_normalized = depth_map.astype(np.float32) / 255.0
        depth_scaled = depth_normalized * self.max_depth
        
        cx, cy = width / 2.0, height / 2.0
        fx, fy = self.focal_length, self.focal_length
        
        u, v = np.meshgrid(np.arange(width), np.arange(height))
        
        z = depth_scaled
        x = (u - cx) * z / fx
        y = (v - cy) * z / fy
        
        points = np.stack([x, y, -z], axis=-1).reshape(-1, 3)
        colors = rgb_image.reshape(-1, 3).astype(np.float32) / 255.0
        
        valid_mask = (z.flatten() > 0.1) & (z.flatten() < self.max_depth)
        points = points[valid_mask]
        colors = colors[valid_mask]
        
        return {
            'points': points,
            'colors': colors,
            'count': len(points),
            'bounds': {
                'min': points.min(axis=0).tolist(),
                'max': points.max(axis=0).tolist()
            }
        }
    
    def generate_mesh(self, pointcloud_data, simplification_ratio=0.5):
        """
        Generate triangulated mesh from point cloud for smoother rendering
        
        Args:
            pointcloud_data: Output from depth_to_pointcloud
            simplification_ratio: Ratio of points to keep (0-1)
            
        Returns:
            Dictionary with vertices, faces, and colors
        """
        points = pointcloud_data['points']
        colors = pointcloud_data['colors']
        
        if simplification_ratio < 1.0:
            num_points = int(len(points) * simplification_ratio)
            indices = np.random.choice(len(points), num_points, replace=False)
            points = points[indices]
            colors = colors[indices]
        
        points_2d = points[:, :2]
        
        try:
            tri = Delaunay(points_2d)
            faces = tri.simplices
            
            edge_lengths = np.sqrt(np.sum(
                (points[faces[:, 0]] - points[faces[:, 1]])**2, axis=1
            ))
            valid_faces = faces[edge_lengths < 0.5]
            
            return {
                'vertices': points.tolist(),
                'faces': valid_faces.tolist(),
                'colors': colors.tolist(),
                'metadata': {
                    'vertex_count': len(points),
                    'face_count': len(valid_faces)
                }
            }
            
        except Exception as e:
            logger.warning(f"Mesh generation failed: {e}. Returning point cloud only.")
            return {
                'vertices': points.tolist(),
                'faces': [],
                'colors': colors.tolist(),
                'metadata': {
                    'vertex_count': len(points),
                    'face_count': 0
                }
            }
    
    def export_threejs_format(self, pointcloud_data, output_path, include_mesh=True):
        """
        Export point cloud in optimized Three.js format
        
        Args:
            pointcloud_data: Output from depth_to_pointcloud
            output_path: Path to save JSON file
            include_mesh: Whether to generate mesh data
            
        Returns:
            Path to exported file
        """
        output_data = {
            'type': 'PointCloud',
            'points': pointcloud_data['points'].tolist(),
            'colors': pointcloud_data['colors'].tolist(),
            'metadata': {
                'count': pointcloud_data['count'],
                'bounds': pointcloud_data['bounds']
            }
        }
        
        if include_mesh:
            mesh_data = self.generate_mesh(pointcloud_data)
            output_data['mesh'] = mesh_data
            output_data['type'] = 'Mesh'
        
        output_path = Path(output_path)
        with open(output_path, 'w') as f:
            json.dump(output_data, f, separators=(',', ':'))
        
        file_size_mb = output_path.stat().st_size / (1024 * 1024)
        logger.info(f"Exported to {output_path.name} ({file_size_mb:.2f} MB)")
        
        return output_path
    
    def export_compressed(self, pointcloud_data, output_path):
        """
        Export highly compressed version for web delivery
        Uses numpy compressed format
        
        Args:
            pointcloud_data: Output from depth_to_pointcloud
            output_path: Path to save compressed file
            
        Returns:
            Path to exported file
        """
        output_path = Path(output_path)
        
        np.savez_compressed(
            output_path,
            points=pointcloud_data['points'].astype(np.float32),
            colors=pointcloud_data['colors'].astype(np.float32),
            bounds=np.array([
                pointcloud_data['bounds']['min'],
                pointcloud_data['bounds']['max']
            ])
        )
        
        return output_path


def process_frame_to_pointcloud(frame_path, depth_path, output_dir, 
                                focal_length=525.0, downsample=2, 
                                include_mesh=True):
    """
    Complete pipeline: frame + depth map -> Three.js point cloud
    
    Args:
        frame_path: Path to original RGB frame
        depth_path: Path to depth map
        output_dir: Directory to save outputs
        focal_length: Camera focal length
        downsample: Downsampling factor for performance
        include_mesh: Whether to generate mesh
        
    Returns:
        Tuple of (pointcloud_data, json_path)
    """
    rgb = cv2.imread(str(frame_path))
    if rgb is None:
        raise ValueError(f"Failed to load frame: {frame_path}")
    
    rgb = cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB)
    
    depth = cv2.imread(str(depth_path), cv2.IMREAD_GRAYSCALE)
    if depth is None:
        raise ValueError(f"Failed to load depth map: {depth_path}")
    
    generator = PointCloudGenerator(focal_length=focal_length)
    
    pointcloud_data = generator.depth_to_pointcloud(
        depth, 
        rgb, 
        downsample_factor=downsample
    )
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    stem = Path(frame_path).stem
    json_path = output_dir / f"{stem}.json"
    
    generator.export_threejs_format(
        pointcloud_data, 
        json_path, 
        include_mesh=include_mesh
    )
    
    logger.info(f"Processed {stem}: {pointcloud_data['count']} points")
    
    return pointcloud_data, json_path