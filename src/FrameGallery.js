import React, { useEffect, useState } from "react";
import API from "../api";
import FrameCard from "./FrameCard";

const FrameGallery = ({ refresh }) => {
  const [frames, setFrames] = useState([]);
  useEffect(() => {
    API.get("/frames/").then((res) => setFrames(res.data.frames));
  }, [refresh]);
  return (
    <section>
      <h2>Extracted Frames</h2>
      <div style={{ display: "flex", flexWrap: "wrap" }}>
        {frames.map((f, i) => (
          <FrameCard key={i} frame={f} />
        ))}
      </div>
    </section>
  );
};
export default FrameGallery;