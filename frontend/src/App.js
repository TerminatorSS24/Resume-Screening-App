import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [jobDesc, setJobDesc] = useState("");
  const [prediction, setPrediction] = useState(null);
  const [atsScore, setAtsScore] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return alert("Please upload a file.");

    const formData = new FormData();
    formData.append("resume", file);
    formData.append("job_description", jobDesc);

    setLoading(true);
    try {
      const res = await axios.post("http://localhost:5000/predict", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setPrediction(res.data.category);
      if (res.data.ats_score !== null) {
        setAtsScore(res.data.ats_score);
      } else {
        setAtsScore(null);
      }
    } catch (err) {
      alert("Error: " + (err.response?.data?.error || err.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <h1>🧠 Resume Screening App</h1>
      <form onSubmit={handleUpload}>
        <input
          type="file"
          accept=".pdf,.docx,.txt"
          onChange={(e) => setFile(e.target.files[0])}
        />
        <textarea
          placeholder="📄 Paste the job description here (optional)"
          value={jobDesc}
          onChange={(e) => setJobDesc(e.target.value)}
        />
        <button type="submit">Submit Resume</button>
      </form>
      {loading && <p>🔄 Analyzing your resume...</p>}
      {prediction && (
        <div className="result">
          <h3>🗂️ Predicted Category:</h3>
          <p>{prediction}</p>
        </div>
      )}
      {atsScore !== null && (
        <div className="result">
          <h3>🔍 ATS Match Score:</h3>
          <p>{atsScore}%</p>
        </div>
      )}
    </div>
  );
}

export default App;
