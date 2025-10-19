from typing import Dict, Optional, List
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FirebaseService:
    """
    Mock Firebase service for testing without credentials
    Person 3 will replace this with real Firebase
    """
    
    def __init__(self):
        self.mock_data = {}
        logger.info("Firebase mock mode initialized")
    
    def store_video_metadata(self, video_id: str, data: Dict) -> bool:
        logger.info(f"[MOCK] Storing metadata for {video_id}")
        self.mock_data[video_id] = data
        return True
    
    def get_video_metadata(self, video_id: str) -> Optional[Dict]:
        logger.info(f"[MOCK] Getting metadata for {video_id}")
        return self.mock_data.get(video_id)
    
    def update_video_status(self, video_id: str, status: str) -> bool:
        logger.info(f"[MOCK] Updating status for {video_id}: {status}")
        if video_id in self.mock_data:
            self.mock_data[video_id]['status'] = status
        return True
    
    def store_scene_data(self, video_id: str, scene_id: str, data: Dict) -> bool:
        logger.info(f"[MOCK] Storing scene {scene_id} for {video_id}")
        return True
    
    def get_all_scenes(self, video_id: str) -> List[Dict]:
        logger.info(f"[MOCK] Getting scenes for {video_id}")
        return []
    
    def store_frame_urls(self, video_id: str, frame_urls: List[str]) -> bool:
        logger.info(f"[MOCK] Storing {len(frame_urls)} frame URLs for {video_id}")
        if video_id in self.mock_data:
            self.mock_data[video_id]['frame_urls'] = frame_urls
        return True
    
    def store_pointcloud_urls(self, video_id: str, pointcloud_urls: List[str]) -> bool:
        logger.info(f"[MOCK] Storing {len(pointcloud_urls)} point cloud URLs for {video_id}")
        if video_id in self.mock_data:
            self.mock_data[video_id]['pointcloud_urls'] = pointcloud_urls
        return True
    
    def delete_video_data(self, video_id: str) -> bool:
        logger.info(f"[MOCK] Deleting data for {video_id}")
        if video_id in self.mock_data:
            del self.mock_data[video_id]
        return True


firebase_service = FirebaseService()