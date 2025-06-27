# 🎬 Video Frame Feature Vector Search with FastAPI

A robust, production-ready FastAPI application for extracting frames from videos, computing feature vectors, and enabling visual similarity search with a modern vector database (Qdrant).

---

## 🚩 Why This Project?

- **Modern AI Demo**: Showcases vector search, video/image processing, and API integration.
- **Recruiter-Ready**: No login required, easy to run, and simple to extend.
- **Production Practices**: Clean code, error handling, logging, and deployment-friendly.

---

## ✨ Features

- **Video Upload**: Extract frames from videos at custom intervals.
- **Vector Storage**: Store frame features in Qdrant for fast similarity search.
- **Visual Search**: Upload an image to find similar frames.
- **REST API**: Well-documented endpoints via FastAPI.
- **Easy Deploy**: Run locally or in the cloud (Railway, Render, Docker).

---

## 🏗️ Project Structure

```
backend/
├── main.py
├── config.py
├── requirements.txt
├── .env.example
├── app/
│   ├── vector_utils.py
│   ├── frame_extractor.py
│   └── models.py
```

---

## ⚡ Quickstart

### 1. Clone & Configure

```bash
git clone https://github.com/imsiddharthnegi/FASTAPI.git
cd FASTAPI/backend
cp .env.example .env  # Adjust settings as needed
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Start Qdrant (Vector DB)

You can run [Qdrant](https://qdrant.tech/) locally with Docker:
```bash
docker run -p 6333:6333 qdrant/qdrant
```

### 4. Launch API

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🛠️ API Endpoints

| Method | Endpoint                         | Description                              |
|--------|----------------------------------|------------------------------------------|
| POST   | `/api/upload_video/`             | Upload video, extract frames             |
| GET    | `/api/frames/`                   | List all extracted frames                |
| GET    | `/api/frame/{dir}/{frame_id}`    | Retrieve a frame image                   |
| POST   | `/api/search_by_image/`          | Upload image, search similar frames      |
| GET    | `/api/search_frames/`            | Search frames by vector                  |

---

## 🔒 Security & Auth

_No authentication is used so recruiters and reviewers can test it easily.  
For production, add authentication and rate limiting._

---

## 📃 License

This project is licensed under the MIT License.  
See the [LICENSE](./LICENSE) file for details.

---

**Made with ❤️ by Siddharth Negi**
