

import { useState } from "react";
import axios from "axios";

export default function Home() {
  const [file, setFile] = useState(null);
  const [jobId, setJobId] = useState("");
  const [status, setStatus] = useState("");
  const [output, setOutput] = useState("");

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("file", file);
    const res = await axios.post("http://localhost:8000/upload", formData);
    setJobId(res.data.job_id);
    setStatus("Uploaded. Processing...");
  };

  const checkStatus = async () => {
    const res = await axios.get(`http://localhost:8000/status/${jobId}`);
    setStatus(`Job ${jobId} status: ${res.data.status}`);
    if (res.data.output) {
      setOutput(res.data.output);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center p-8">
      <h1 className="text-3xl font-bold mb-4">AI Content Repurposer</h1>

      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
        className="mb-4"
      />

      <button
        onClick={handleUpload}
        className="bg-blue-600 text-white px-4 py-2 rounded mb-4"
      >
        Upload & Start
      </button>

      <input
        type="text"
        placeholder="Enter Job ID"
        value={jobId}
        onChange={(e) => setJobId(e.target.value)}
        className="border p-2 mb-2"
      />

      <button
        onClick={checkStatus}
        className="bg-green-600 text-white px-4 py-2 rounded"
      >
        Check Status
      </button>

      <p className="mt-4 text-lg">{status}</p>

      {output && (
        <div className="mt-4 w-full max-w-xl p-4 bg-white rounded shadow">
          <h2 className="text-xl font-semibold mb-2">AI Output</h2>
          <pre className="whitespace-pre-wrap text-sm">{output}</pre>
        </div>
      )}
    </div>
  );
      }
