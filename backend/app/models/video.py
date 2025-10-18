from pydantic import BaseModel
from typing import List, Optional

class VideoMetadata(BaseModel):
    video_id: str
    filename: str
    video_url: str
    status: str

class SceneObject(BaseModel):
    name: str
    confidence: float
    timestamp: float

class SceneData(BaseModel):
    scene_id: str
    timestamp: float
    objects: List[SceneObject]
    transcript: Optional[str]
    caption: Optional[str]
