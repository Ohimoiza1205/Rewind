import numpy as np
import cv2
from scipy.ndimage import gaussian_filter
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DepthOptimizer:
    """
    Advanced depth map optimization for higher quality 3D reconstruction
    Includes smoothing, hole filling, and edge preservation
    """
    
    @staticmethod
    def smooth_depth(depth_map, kernel_size=5, sigma=1.0):
        """
        Apply Gaussian smoothing to depth map while preserving edges
        
        Args:
            depth_map: Input depth map
            kernel_size: Gaussian kernel size
            sigma: Gaussian sigma
            
        Returns:
            Smoothed depth map
        """
        smoothed = gaussian_filter(depth_map.astype(np.float32), sigma=sigma)
        return smoothed.astype(depth_map.dtype)
    
    @staticmethod
    def fill_holes(depth_map, method='inpaint'):
        """
        Fill holes and invalid regions in depth map
        
        Args:
            depth_map: Input depth map
            method: Filling method ('inpaint' or 'bilateral')
            
        Returns:
            Depth map with filled holes
        """
        mask = (depth_map == 0).astype(np.uint8)
        
        if method == 'inpaint':
            filled = cv2.inpaint(
                depth_map, 
                mask, 
                inpaintRadius=3, 
                flags=cv2.INPAINT_TELEA
            )
        else:
            filled = cv2.bilateralFilter(depth_map, 9, 75, 75)
        
        return filled
    
    @staticmethod
    def enhance_edges(depth_map, rgb_image=None):
        """
        Enhance depth discontinuities at object boundaries
        
        Args:
            depth_map: Input depth map
            rgb_image: Optional RGB image for guided filtering
            
        Returns:
            Edge-enhanced depth map
        """
        if rgb_image is not None:
            enhanced = cv2.ximgproc.guidedFilter(
                guide=rgb_image,
                src=depth_map,
                radius=8,
                eps=100
            )
        else:
            edges = cv2.Canny(depth_map, 50, 150)
            kernel = np.ones((3,3), np.uint8)
            edges_dilated = cv2.dilate(edges, kernel, iterations=1)
            
            enhanced = depth_map.copy()
            enhanced[edges_dilated > 0] = depth_map[edges_dilated > 0]
        
        return enhanced
    
    @staticmethod
    def temporal_smoothing(depth_maps, window_size=3):
        """
        Apply temporal smoothing across consecutive depth maps
        
        Args:
            depth_maps: List of consecutive depth maps
            window_size: Temporal window size
            
        Returns:
            List of temporally smoothed depth maps
        """
        smoothed_maps = []
        
        for i in range(len(depth_maps)):
            start_idx = max(0, i - window_size // 2)
            end_idx = min(len(depth_maps), i + window_size // 2 + 1)
            
            window = depth_maps[start_idx:end_idx]
            averaged = np.mean(window, axis=0).astype(depth_maps[i].dtype)
            smoothed_maps.append(averaged)
        
        return smoothed_maps
    
    @staticmethod
    def optimize_for_threejs(depth_map, target_percentile=95):
        """
        Optimize depth range for Three.js rendering
        
        Args:
            depth_map: Input depth map
            target_percentile: Percentile for depth clipping
            
        Returns:
            Optimized depth map with better distribution
        """
        depth_float = depth_map.astype(np.float32)
        
        non_zero = depth_float[depth_float > 0]
        
        if len(non_zero) == 0:
            return depth_map
        
        max_depth = np.percentile(non_zero, target_percentile)
        
        depth_clipped = np.clip(depth_float, 0, max_depth)
        
        depth_normalized = (depth_clipped / max_depth * 255).astype(np.uint8)
        
        return depth_normalized
    
    @staticmethod
    def apply_full_optimization(depth_map, rgb_image=None):
        """
        Apply complete optimization pipeline
        
        Args:
            depth_map: Input depth map
            rgb_image: Optional RGB image for guided filtering
            
        Returns:
            Fully optimized depth map
        """
        logger.info("Applying depth optimization pipeline")
        
        optimized = DepthOptimizer.smooth_depth(depth_map, kernel_size=5, sigma=1.0)
        
        optimized = DepthOptimizer.fill_holes(optimized, method='inpaint')
        
        if rgb_image is not None:
            try:
                optimized = DepthOptimizer.enhance_edges(optimized, rgb_image)
            except AttributeError:
                logger.warning("Guided filtering not available, skipping edge enhancement")
        
        optimized = DepthOptimizer.optimize_for_threejs(optimized)
        
        return optimized