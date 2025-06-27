# 🎬 Video Frame Feature Vector Search

A full-stack, production-ready application that extracts frames from videos, computes feature vectors for each frame, and enables visual similarity search using a modern vector database.

---

## 🚀 Features

- **Video Upload**: Upload MP4 files and extract frames at custom intervals.
- **Frame Gallery**: View all extracted frames in a browsable gallery.
- **Vector Storage**: Compute color histogram feature vectors and store them in [Qdrant](https://qdrant.tech/) for fast similarity search.
- **Visual Search**: Upload an image to find visually similar frames.
- **REST API**: Clean, typed, and documented endpoints using [FastAPI](https://fastapi.tiangolo.com/).
- **Modern Frontend**: Responsive UI built with [React](https://react.dev/).
- **Production Ready**: Modular, maintainable code structure, proper error handling, and clear logging.
- **Deployment Friendly**: Easily deployable with Docker, Railway, Vercel, Netlify, or your favorite cloud.

---

## 🏗️ Architecture

```
[React Frontend] ←→ [FastAPI Backend] ←→ [Qdrant Vector DB]
             ↑                        ↑
     (Video, image uploads)   (Frame extraction, search)
```

---

## 📂 Directory Structure

```
project-root/
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── requirements.txt
│   ├── .env.example
│   └── app/
│       ├── vector_utils.py
│       ├── frame_extractor.py
│       └── models.py
├── frontend/
│   └── ... (see frontend/README.md)
├── qdrant/
│   └── docker-compose.yml
├── .gitignore
├── README.md
```

---

## ⚡ Quick Start

### 1. Start Qdrant (Vector DB)

```bash
cd qdrant
docker-compose up -d
```

### 2. Backend Setup

```bash
cd backend
cp .env.example .env    # Edit as needed!
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup

```bash
cd frontend
npm install
npm start
```

The frontend will run at [http://localhost:3000](http://localhost:3000).

---

## 🛠️ API Endpoints

| Method | Endpoint                         | Description                              |
|--------|----------------------------------|------------------------------------------|
| POST   | `/api/upload_video/`             | Upload a video, extract/store frames     |
| GET    | `/api/frames/`                   | List all extracted frames                |
| GET    | `/api/frame/{dir}/{frame_id}`    | Retrieve a specific frame image          |
| POST   | `/api/search_by_image/`          | Upload image, search similar frames      |
| GET    | `/api/search_frames/`            | Search frames by vector                  |

Interactive docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🌐 Deployment

- **Backend:** Railway, Render, or Docker
- **Frontend:** Vercel or Netlify
- **Qdrant:** Qdrant Cloud, Railway, or self-hosted Docker

> **Note:** Set correct CORS origins and backend URLs in your `.env` files for production!

---

## 💡 Why This Project Stands Out

- **Modern Vector Search**: Uses Qdrant—state-of-the-art for AI similarity.
- **Clean Code**: Modular Python, type-checked, with clear separation of concerns.
- **Professional API**: FastAPI delivers OpenAPI docs, validation, and easy testing.
- **Frontend Polish**: Responsive, accessible, with clear user feedback.
- **Deployable Anywhere**: Docker support and cloud deployment instructions.
- **Recruiter-Friendly Demo**: No login required—easy for anyone to try!

---

## 🔒 Security

This demo **intentionally does not use authentication** to simplify recruiter testing.  
For production, add authentication and rate limiting.

---

## 📢 Demo Instructions for Recruiters

1. **Open the frontend URL** (see deployment section).
2. **Upload a video** (MP4 format), wait for frame extraction.
3. **View** the extracted frames in the gallery.
4. **Try visual search**: upload an image to find similar frames.
5. See [API docs](http://localhost:8000/docs) for more.

---

## 📝 License

MIT © [Your Name](mailto:your@email.com)

---

## 🙋‍♂️ Contact

For questions or feedback, open an issue or contact [Your Name](mailto:your@email.com).