import React, { useState } from "react";
import API from "../api";

const API_URL = process.env.REACT_APP_BACKEND_URL || "http://localhost:8000/api";

const ImageSearch = () => {
  const [file, setFile] = useState(null);
  const [results, setResults] = useState([]);
  const [status, setStatus] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return setStatus("Select an image first.");
    setStatus("Searching...");
    const data = new FormData();
    data.append("file", file);
    try {
      const res = await API.post("/search_by_image/", data);
      setResults(res.data);
      setStatus("");
    } catch {
      setStatus("Search failed.");
    }
  };

  return (
    <section>
      <h2>Search Similar Frames by Image</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="file"
          accept="image/*"
          onChange={(e) => setFile(e.target.files[0])}
        />
        <button type="submit" style={{ marginLeft: "10px" }}>Search</button>
      </form>
      <div>{status}</div>
      <div style={{ display: "flex", flexWrap: "wrap" }}>
        {results.map((r, i) => (
          <div key={i} style={{ margin: 8 }}>
            <img
              src={`${API_URL}/frame/${r.dir}/${r.frame_id}`}
              alt={r.frame_id}
              style={{ width: 120, borderRadius: 3 }}
            />
            <div style={{ fontSize: 12 }}>Score: {r.score.toFixed(3)}</div>
          </div>
        ))}
      </div>
    </section>
  );
};

export default ImageSearch;