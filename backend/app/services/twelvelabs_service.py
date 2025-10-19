from twelvelabs import TwelveLabs
from app.config import settings

client = TwelveLabs(api_key=settings.TL_API_KEY)

def create_index(name="rewind-index"):
    index = client.indexes.create(
        index_name=name,
        models=[
            {
                "model_name": "marengo2.7",
                "model_options": ["visual", "audio"]
            }
        ]
    )
    return index

def upload_video_to_twelvelabs(video_url: str, index_id: str):
    # Fixed: Use video_url parameter name
    task = client.tasks.create(
        index_id=index_id,
        video_url=video_url  # Changed from url to video_url
    )
    return task

def get_task_status(task_id: str):
    task = client.tasks.retrieve(task_id)
    return task.status

def get_video_analysis(index_id: str, video_id: str):
    video = client.indexes.videos.retrieve(index_id, video_id)
    return video

def search_video(index_id: str, query: str):
    results = client.search.query(
        index_id=index_id,
        query_text=query,
        options=["visual"]
    )
    return results

def list_indexes():
    return client.indexes.list()    
