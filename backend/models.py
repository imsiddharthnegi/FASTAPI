"""
Typed API response/request models.
"""

from typing import List, Optional
from pydantic import BaseModel

class FrameInfo(BaseModel):
    frame_id: str
    dir: str

class SearchResult(BaseModel):
    score: float
    frame_id: str
    dir: str
    feature_vector: Optional[List[float]] = None

class UploadResponse(BaseModel):
    frames: List[str]
    dir: str
    count: int

class FrameListResponse(BaseModel):
    frames: List[FrameInfo]