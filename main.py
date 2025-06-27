import os
import shutil
import uuid
from typing import List
from fastapi import FastAPI, UploadFile, File, Form, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

import cv2
import numpy as np
from PIL import Image

from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, Filter, FieldCondition, MatchValue

# Settings
OUTPUT_DIR = "output_frames"
VECTOR_DIM = 256 * 3  # 256 bins per channel, 3 channels

QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
QDRANT_COLLECTION = "frames"

# Init FastAPI and Qdrant
app = FastAPI(title="Video Frame Feature Vector Search API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

def ensure_collection():
    if QDRANT_COLLECTION not in [c.name for c in client.get_collections().collections]:
        client.recreate_collection(
            collection_name=QDRANT_COLLECTION,
            vectors_config={"size": VECTOR_DIM, "distance": "Cosine"}
        )

ensure_collection()

def extract_frames(video_path: str, interval_sec: int, output_dir: str) -> List[str]:
    os.makedirs(output_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_list = []
    frame_count = 0
    success = True
    while success:
        success, frame = cap.read()
        if not success:
            break
        if int(frame_count % int(fps * interval_sec)) == 0:
            img_path = os.path.join(output_dir, f"frame_{frame_count}.jpg")
            cv2.imwrite(img_path, frame)
            frame_list.append(img_path)
        frame_count += 1
    cap.release()
    return frame_list

def compute_histogram(image_path: str) -> np.ndarray:
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not open image {image_path}")
    chans = cv2.split(img)
    features = []
    for chan in chans:
        hist = cv2.calcHist([chan], [0], None, [256], [0, 256]).flatten()
        hist = hist / hist.sum()  # normalize
        features.extend(hist)
    return np.array(features, dtype=np.float32)

@app.post("/upload_video/")
async def upload_video(
    file: UploadFile = File(...),
    interval: int = Form(1)
):
    # Save uploaded file
    temp_video = f"temp_{uuid.uuid4()}.mp4"
    with open(temp_video, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Extract frames
    frames_dir = os.path.join(OUTPUT_DIR, str(uuid.uuid4()))
    frames = extract_frames(temp_video, interval, frames_dir)
    os.remove(temp_video)

    # Compute feature vectors and index in Qdrant
    points = []
    for fpath in frames:
        vec = compute_histogram(fpath)
        frame_id = os.path.basename(fpath)
        points.append(PointStruct(
            id=frame_id,
            vector=vec.tolist(),
            payload={"frame_path": fpath}
        ))

    client.upsert(
        collection_name=QDRANT_COLLECTION,
        points=points
    )
    return {"frames_saved": frames, "count": len(frames)}

@app.get("/frame/{frame_id}")
def get_frame(frame_id: str):
    # Find frame in output dir
    for root, _, files in os.walk(OUTPUT_DIR):
        if frame_id in files:
            return FileResponse(os.path.join(root, frame_id))
    return {"error": "Frame not found"}

@app.get("/search_frames/")
def search_frames(
    feature_vector: List[float] = Query(..., description="Flattened feature vector"),
    top_k: int = 5
):
    # Search Qdrant
    results = client.search(
        collection_name=QDRANT_COLLECTION,
        query_vector=feature_vector,
        limit=top_k
    )
    # Return frame image URLs and vectors
    resp = []
    for r in results:
        resp.append({
            "score": r.score,
            "frame_id": r.id,
            "frame_path": r.payload.get("frame_path"),
            "feature_vector": r.vector
        })
    return resp

@app.get("/")
def read_root():
    return {"msg": "FastAPI Video Frame Vector Search! See /docs for API."}