import torch
import cv2
import numpy as np
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DepthEstimator:
    """
    High-quality depth estimation using MiDaS models
    Supports multiple model types with automatic device selection
    """
    
    def __init__(self, model_type="DPT_Large", device=None):
        """
        Initialize depth estimator with specified model
        
        Args:
            model_type: Model architecture - "DPT_Large", "DPT_Hybrid", or "MiDaS_small"
            device: Torch device (auto-detects CUDA if available)
        """
        self.device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Initializing DepthEstimator on device: {self.device}")
        
        try:
            self.midas = torch.hub.load("intel-isl/MiDaS", model_type, trust_repo=True)
            self.midas.to(self.device)
            self.midas.eval()
            
            midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms", trust_repo=True)
            
            if model_type in ["DPT_Large", "DPT_Hybrid"]:
                self.transform = midas_transforms.dpt_transform
            else:
                self.transform = midas_transforms.small_transform
            
            logger.info(f"Successfully loaded {model_type}")
            
        except Exception as e:
            logger.error(f"Failed to load MiDaS model: {e}")
            raise
    
    def estimate_depth(self, image_path, normalize=True):
        """
        Estimate depth map from single image with high precision
        
        Args:
            image_path: Path to input image
            normalize: Whether to normalize depth to 0-255 range
            
        Returns:
            depth_map: Depth map as numpy array (normalized or raw)
        """
        try:
            img = cv2.imread(str(image_path))
            if img is None:
                raise ValueError(f"Failed to load image: {image_path}")
            
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            input_batch = self.transform(img_rgb).to(self.device)
            
            with torch.no_grad():
                prediction = self.midas(input_batch)
                
                prediction = torch.nn.functional.interpolate(
                    prediction.unsqueeze(1),
                    size=img_rgb.shape[:2],
                    mode="bicubic",
                    align_corners=False,
                ).squeeze()
            
            depth_map = prediction.cpu().numpy()
            
            if normalize:
                depth_map = cv2.normalize(
                    depth_map, 
                    None, 
                    0, 
                    255, 
                    cv2.NORM_MINMAX, 
                    cv2.CV_8U
                )
            
            return depth_map
            
        except Exception as e:
            logger.error(f"Error estimating depth for {image_path}: {e}")
            raise
    
    def estimate_batch(self, image_paths, output_dir):
        """
        Process multiple images with progress tracking
        
        Args:
            image_paths: List of image file paths
            output_dir: Directory to save depth maps
            
        Returns:
            List of output paths
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_paths = []
        
        for i, img_path in enumerate(image_paths):
            logger.info(f"Processing {i+1}/{len(image_paths)}: {img_path.name}")
            
            depth = self.estimate_depth(img_path)
            
            output_path = output_dir / f"{img_path.stem}_depth.png"
            cv2.imwrite(str(output_path), depth)
            output_paths.append(output_path)
        
        logger.info(f"Batch processing complete. Saved to {output_dir}")
        return output_paths