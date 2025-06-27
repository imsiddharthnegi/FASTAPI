"""
Video frame extraction utilities.
"""

import os
import cv2
from typing import List

def extract_frames(video_path: str, interval_sec: int, output_dir: str) -> List[str]:
    """
    Extract frames from a video file every interval_sec seconds.
    Returns a list of saved frame image paths.
    """
    os.makedirs(output_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 25  # Fallback to 25 fps if not detected
    frame_list: List[str] = []
    frame_count = 0
    success, frame = cap.read()
    while success:
        if int(frame_count % int(fps * interval_sec)) == 0:
            img_path = os.path.join(output_dir, f"frame_{frame_count}.jpg")
            cv2.imwrite(img_path, frame)
            frame_list.append(img_path)
        frame_count += 1
        success, frame = cap.read()
    cap.release()
    return frame_list