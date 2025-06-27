"""
Video Frame Vector Search API – FastAPI entrypoint.

Handles video uploads, frame extraction, feature vectorization,
and similarity search using Qdrant vector database.

Author: imsiddharthnegi
"""

import os
import shutil
import uuid
import logging
from typing import List

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct

from app.vector_utils import compute_histogram
from app.frame_extractor import extract_frames
from app.models import FrameInfo, SearchResult, UploadResponse, FrameListResponse
from config import settings

# --- Logging Configuration ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("vector_search_api")

os.makedirs(settings.OUTPUT_DIR, exist_ok=True)

app = FastAPI(
    title="Video Frame Feature Vector Search API",
    description="Upload videos, extract frames, and visually search for similar frames using Qdrant vector DB.",
    version="1.1.0"
)

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS if settings.ALLOWED_ORIGINS != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_qdrant_client() -> QdrantClient:
    """
    Helper to get a Qdrant client instance.
    """
    return QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)

def ensure_collection(client: QdrantClient):
    """
    Ensure the Qdrant collection for storing frame vectors exists.
    """
    collections = [c.name for c in client.get_collections().collections]
    if settings.QDRANT_COLLECTION not in collections:
        logger.info("Collection '%s' not found. Creating...", settings.QDRANT_COLLECTION)
        client.recreate_collection(
            collection_name=settings.QDRANT_COLLECTION,
            vectors_config={"size": settings.VECTOR_DIM, "distance": "Cosine"},
        )
        logger.info("Collection '%s' created.", settings.QDRANT_COLLECTION)

@app.on_event("startup")
def startup_event():
    logger.info("Starting up. Connecting to Qdrant at %s:%s", settings.QDRANT_HOST, settings.QDRANT_PORT)
    client = get_qdrant_client()
    ensure_collection(client)
    logger.info("Qdrant vector collection ready.")

@app.post("/api/upload_video/", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_video(
    file: UploadFile = File(..., description="MP4 video file"),
    interval: int = Form(1, description="Frame extraction interval in seconds (default: 1)")
):
    """
    Upload a video, extract frames every 'interval' seconds,
    compute feature vectors, and store in Qdrant.
    """
    temp_video = f"temp_{uuid.uuid4()}.mp4"
    try:
        with open(temp_video, "wb") as fobj:
            shutil.copyfileobj(file.file, fobj)
        frames_dir = os.path.join(settings.OUTPUT_DIR, str(uuid.uuid4()))
        frames = extract_frames(temp_video, interval, frames_dir)
        if not frames:
            raise HTTPException(
                status_code=400,
                detail="No frames could be extracted from the provided video."
            )
        client = get_qdrant_client()
        points = []
        for fpath in frames:
            try:
                vec = compute_histogram(fpath)
            except Exception as e:
                logger.error("Failed to compute vector for frame %s: %s", fpath, e)
                continue
            frame_id = os.path.basename(fpath)
            points.append(PointStruct(
                id=frame_id,
                vector=vec.tolist(),
                payload={"frame_path": fpath, "dir": os.path.basename(frames_dir)}
            ))
        if points:
            client.upsert(
                collection_name=settings.QDRANT_COLLECTION,
                points=points
            )
        logger.info("Video uploaded: %s | Frames extracted: %d", file.filename, len(frames))
        return UploadResponse(frames=[os.path.basename(f) for f in frames], dir=os.path.basename(frames_dir), count=len(frames))
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Unexpected error during video upload.")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred during video processing."
        )
    finally:
        if os.path.exists(temp_video):
            os.remove(temp_video)

@app.get("/api/frames/", response_model=FrameListResponse)
def list_frames():
    """
    List all extracted frames currently available in the output directory.
    """
    frames = []
    for root, _, files in os.walk(settings.OUTPUT_DIR):
        for file in files:
            if file.endswith(".jpg"):
                rel_dir = os.path.basename(root)
                frames.append(FrameInfo(frame_id=file, dir=rel_dir))
    return FrameListResponse(frames=frames)

@app.get("/api/frame/{dir}/{frame_id}", responses={404: {"description": "Frame not found"}})
def get_frame(dir: str, frame_id: str):
    """
    Retrieve a specific frame image by directory and frame id.
    """
    path = os.path.join(settings.OUTPUT_DIR, dir, frame_id)
    if not os.path.exists(path):
        logger.warning("Frame not found: %s", path)
        raise HTTPException(404, detail="Frame not found.")
    return FileResponse(path, media_type="image/jpeg")

@app.post("/api/search_by_image/", response_model=List[SearchResult])
async def search_by_image(
    file: UploadFile = File(..., description="Query image file (jpg/png)"),
    top_k: int = Form(5, description="How many similar frames to return")
):
    """
    Upload an image and search for the top_k visually similar frames.
    """
    img_path = f"temp_query_{uuid.uuid4()}.jpg"
    try:
        with open(img_path, "wb") as fobj:
            shutil.copyfileobj(file.file, fobj)
        vec = compute_histogram(img_path).tolist()
        client = get_qdrant_client()
        results = client.search(
            collection_name=settings.QDRANT_COLLECTION,
            query_vector=vec,
            limit=top_k
        )
        return [
            SearchResult(
                score=r.score,
                frame_id=r.id,
                dir=r.payload.get("dir"),
                feature_vector=r.vector
            ) for r in results
        ]
    except Exception as exc:
        logger.exception("Failed to search by image.")
        raise HTTPException(
            status_code=500,
            detail="Failed to perform image similarity search."
        )
    finally:
        if os.path.exists(img_path):
            os.remove(img_path)

@app.get("/api/search_frames/", response_model=List[SearchResult])
def search_frames(
    feature_vector: List[float],
    top_k: int = 5
):
    """
    Search for frames similar to the given feature vector.
    """
    try:
        client = get_qdrant_client()
        results = client.search(
            collection_name=settings.QDRANT_COLLECTION,
            query_vector=feature_vector,
            limit=top_k
        )
        return [
            SearchResult(
                score=r.score,
                frame_id=r.id,
                dir=r.payload.get("dir"),
                feature_vector=r.vector
            ) for r in results
        ]
    except Exception as exc:
        logger.exception("Failed to search frames by vector.")
        raise HTTPException(
            status_code=500,
            detail="Failed to search frames by feature vector."
        )

@app.get("/", include_in_schema=False)
def root():
    """API health check endpoint."""
    return {"msg": "Welcome to the Video Frame Feature Vector Search API! See /docs for OpenAPI documentation."}