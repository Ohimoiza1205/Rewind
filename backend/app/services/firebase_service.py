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
    
    def store_pointcloud_urls(self, video_i
    : str, pointcloud_urls: List[str]) -> bool:
        logger.info(f"[MOCK] Storing {len(pointcloud_urls)} point cloud URLs for {video_id}")
        if video_id in self.mock_data:
            self.mock_data[video_id]['pointcloud_urls'] = pointcloud_urls
        return True
    
    def delete_video_data(self, video_id: str) -> bool:
        logger.info(f"[MOCK] Deleting data for {video_id}")
        if video_id in self.mock_data:
            del self.mock_data[video_id]
        return True
    def get_video_analysis(self, video_id: str) -> Optional[Dict]:
        """Get video analysis by video_id"""
        try:
            if self.mock_mode:
                logger.info(f"[MOCK] Getting analysis for {video_id}")
                return self.mock_data.get(f"mock_doc_{video_id}")
            
            docs = self.db.collection('video_analysis').where('video_id', '==', video_id).limit(1).stream()
            for doc in docs:
                return doc.to_dict()
            return None
        except Exception as e:
            logger.error(f"Failed to get analysis: {e}")
            return None
    def save_video_analysis(self, user_id: str, video_id: str, data: Dict) -> str:
        """Save complete video analysis to Firestore"""
        try:
            if self.mock_mode:
                logger.info(f"[MOCK] Saving analysis for {video_id}")
                doc_id = f"mock_doc_{video_id}"
                self.mock_data[doc_id] = data
                return doc_id
            
            doc_ref = self.db.collection('video_analysis').document()
            data['created_at'] = datetime.utcnow()
            data['user_id'] = user_id
            data['video_id'] = video_id
            doc_ref.set(data)
            logger.info(f"Saved analysis: {doc_ref.id}")
            return doc_ref.id
        except Exception as e:
            logger.error(f"Failed to save analysis: {e}")
            raise
firebase_service = FirebaseService()