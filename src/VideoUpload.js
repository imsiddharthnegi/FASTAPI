import React, { useState } from "react";
import API from "../api";

const VideoUpload = ({ onUpload }) => {
  const [interval, setInterval] = useState(1);
  const [status, setStatus] = useState("");

  const handleUpload = async (e) => {
    e.preventDefault();
    setStatus("Processing...");
    const form = e.target;
    const file = form.file.files[0];
    if (!file) return setStatus("No file selected.");
    const data = new FormData();
    data.append("file", file);
    data.append("interval", interval);
    try {
      const res = await API.post("/upload_video/", data, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setStatus(`Extracted ${res.data.count} frames.`);
      onUpload();
    } catch {
      setStatus("Upload failed.");
    }
  };

  return (
    <section>
      <h2>Upload Video</h2>
      <form onSubmit={handleUpload}>
        <input type="file" name="file" accept="video/mp4" required />
        <input
          type="number"
          min="1"
          value={interval}
          onChange={(e) => setInterval(e.target.value)}
          style={{ width: "60px", marginLeft: "10px" }}
        />
        <button type="submit" style={{ marginLeft: "10px" }}>Upload</button>
      </form>
      <div>{status}</div>
    </section>
  );
};
export default VideoUpload;