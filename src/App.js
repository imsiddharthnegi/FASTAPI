import React, { useState } from "react";
import VideoUpload from "./components/VideoUpload";
import FrameGallery from "./components/FrameGallery";
import ImageSearch from "./components/ImageSearch";
import "./App.css";

function App() {
  const [refreshFrames, setRefreshFrames] = useState(false);

  return (
    <div className="App">
      <h1>Video Frame Feature Vector Search</h1>
      <VideoUpload onUpload={() => setRefreshFrames(!refreshFrames)} />
      <ImageSearch />
      <FrameGallery refresh={refreshFrames} />
    </div>
  );
}
export default App;