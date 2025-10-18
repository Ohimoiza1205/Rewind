from twelvelabs import TwelveLabs
from app.config import settings
import os

client = TwelveLabs(api_key=settings.TL_API_KEY)

def create_index():
    index = client.index.create(
        name="rewind-index",
        engines=[
            {
                "name": "marengo2.6",
                "options": ["visual", "conversation", "text_in_video"]
            }
        ]
    )
    return index

def upload_video_to_twelvelabs(video_url: str, index_id: str):
    task = client.task.create(
        index_id=index_id,
        video_url=video_url
    )
    return task

def get_video_analysis(index_id: str, video_id: str):
    video = client.index.video.get(index_id, video_id)
    return video
    
    
    

    
    
    

    
    
