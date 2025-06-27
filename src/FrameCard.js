import React from "react";
const API_URL = process.env.REACT_APP_BACKEND_URL || "http://localhost:8000/api";

const FrameCard = ({ frame }) => (
  <div style={{ margin: 8, border: "1px solid #ccc", borderRadius: 6, padding: 5 }}>
    <img
      src={`${API_URL}/frame/${frame.dir}/${frame.frame_id}`}
      alt={frame.frame_id}
      style={{ width: 140, borderRadius: 4 }}
    />
    <div style={{ fontSize: 12 }}>{frame.frame_id}</div>
  </div>
);

export default FrameCard;