import React, { useState } from 'react';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState('');
  const [previewUrl, setPreviewUrl] = useState('');

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    setPreviewUrl(URL.createObjectURL(selectedFile));
    setStatus('');
  };

 const handleSubmit = async () => {
  if (!file) {
    setStatus('Please select a file first.');
    return;
  }

  const formData = new FormData();
  formData.append('file', file);

  setStatus('Uploading and processing...');

  try {
    const response = await fetch('https://room-report-app-production.up.railway.app/upload', {
      method: 'POST',
      body: formData,
    });

    const contentType = response.headers.get('content-type');

    if (!contentType || !contentType.includes('application/json')) {
      const text = await response.text();
      setStatus(`❌ Invalid JSON response: ${text}`);
      return;
    }

    const result = await response.json();

    if (response.ok) {
      setStatus(`✅ Success! Rows sent: ${result.rows_sent}`);
    } else {
      setStatus(`❌ Error: ${result.error}`);
    }

  } catch (err) {
    setStatus(`❌ Network or server error: ${err.message}`);
  }
};


  return (
    <div className="App">
      <h1>Room Report Uploader</h1>

      <input type="file" accept="image/*" onChange={handleFileChange} />
      {previewUrl && <img src={previewUrl} alt="Preview" style={{ width: '400px', margin: '20px 0' }} />}
      
      <br />
      <button onClick={handleSubmit}>Upload & Send to Google Sheet</button>

      <p>{status}</p>
    </div>
  );
}

export default App;
