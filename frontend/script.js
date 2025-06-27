const API_BASE = "http://localhost:8000"; // Adjust if backend is hosted elsewhere

// Upload video
document.getElementById('uploadForm').onsubmit = async (e) => {
  e.preventDefault();
  const file = document.getElementById('videoInput').files[0];
  const interval = document.getElementById('interval').value;

  const formData = new FormData();
  formData.append('file', file);
  formData.append('interval', interval);

  document.getElementById('uploadStatus').innerText = 'Uploading...';

  const res = await fetch(`${API_BASE}/upload_video/`, {
    method: 'POST',
    body: formData
  });
  const data = await res.json();
  document.getElementById('uploadStatus').innerText = `Extracted ${data.count} frames!`;
};

// Search similar frames
document.getElementById('searchBtn').onclick = async () => {
  const imgFile = document.getElementById('queryImage').files[0];
  if (!imgFile) {
    alert("Select an image first!");
    return;
  }
  // Compute feature vector client-side (simulate by sending to backend or use an extracted frame)
  // For demo, we upload image, backend must provide endpoint to compute and search
  const formData = new FormData();
  formData.append('file', imgFile);

  // You'll need to implement /search_by_image endpoint in backend for this to work fully
  const res = await fetch(`${API_BASE}/search_by_image/`, {
    method: 'POST',
    body: formData
  });
  const results = await res.json();
  const container = document.getElementById('searchResults');
  container.innerHTML = "<h3>Results:</h3>";
  results.forEach(r => {
    const img = document.createElement('img');
    img.src = `${API_BASE}/frame/${r.frame_id}`;
    img.width = 160;
    container.appendChild(img);
    container.appendChild(document.createTextNode(`Score: ${r.score.toFixed(3)}`));
    container.appendChild(document.createElement('br'));
  });
};