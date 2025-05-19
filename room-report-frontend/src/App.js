import React, { useState, useEffect } from 'react';

function App() {
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState('');
  const [status, setStatus] = useState('');

  // ✅ Handle paste event
  useEffect(() => {
    const handlePaste = (event) => {
      const items = event.clipboardData.items;
      for (const item of items) {
        if (item.type.indexOf('image') !== -1) {
          const blob = item.getAsFile();
          const newFile = new File([blob], 'pasted-image.png', { type: blob.type });
          setFile(newFile);
          setPreviewUrl(URL.createObjectURL(newFile));
          setStatus('✅ Image pasted and ready!');
          break;
        }
      }
    };

    window.addEventListener('paste', handlePaste);
    return () => window.removeEventListener('paste', handlePaste);
  }, []);

  const handleSubmit = async () => {
    if (!file) {
      setStatus('❌ No image selected or pasted');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    setStatus('⏳ Uploading...');

    try {
      const response = await fetch('https://room-report-app-production.up.railway.app/upload', {
        method: 'POST',
        body: formData,
      });
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
      <h2>📋 Paste or Upload Room Report Image</h2>

      <input
        type="file"
        accept="image/*"
        onChange={(e) => {
          const selectedFile = e.target.files[0];
          setFile(selectedFile);
          setPreviewUrl(URL.createObjectURL(selectedFile));
          setStatus('');
        }}
      />

      <div style={{ marginTop: '20px' }}>
        {previewUrl && <img src={previewUrl} alt="preview" style={{ width: '400px' }} />}
      </div>

      <p><em>Tip: You can paste a screenshot (Ctrl+V) directly into this page!</em></p>

      <button onClick={handleSubmit} style={{ marginTop: '10px' }}>
        Upload & Send to Google Sheet
      </button>

      <p>{status}</p>
    </div>
  );
}

export default App;