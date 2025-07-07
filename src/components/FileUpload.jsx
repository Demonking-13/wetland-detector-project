import React, { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import axios from "axios";
import "../styles/FileUpload.css";
import { useNavigate } from "react-router-dom";

const FileUpload = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState("");
  const [progress, setProgress] = useState(0);
  const [showProgress, setShowProgress] = useState(false);
  const navigate = useNavigate();

  const onDrop = useCallback((acceptedFiles) => {
    const file = acceptedFiles[0];
    acceptedFiles.map((selectedFile) =>
      Object.assign(selectedFile, { preview: URL.createObjectURL(selectedFile) })
    )
    setSelectedFile(file);
    setUploadStatus("");  // Clear any previous status
    setProgress(0);       // Reset progress
    setShowProgress(false); // Hide progress initially
  }, []);

  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    accept: { 'image/*': ['.jpg', '.jpeg', '.png'] },
    multiple: false,
  });

  const handleUpload = async () => {
    if (!selectedFile) {
      setUploadStatus("Please select an image first.");
      return;
    }

    setShowProgress(true);
    setUploadStatus("Uploading...");


    const formData = new FormData();
    formData.append("image", selectedFile);

    try {
      await axios.post("http://127.0.0.1:5000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
        onUploadProgress: (progressEvent) => {
          const percent = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          setProgress(percent);
        },
      }).then((response) => {
        const { plotted_image, wetland_percentage } = response.data;

        // Show success message
        setUploadStatus(`Upload Successful! `);

        // Simulate delay and redirect
        setTimeout(() => {
          setUploadStatus("Processing...");

          // Step 4: Simulate backend processing (or wait for a response if needed)
          setTimeout(() => {
            // Navigate to result page with state
            navigate("/result", {  // Step 5: Redirect to /result
              state: {
                originalImage: selectedFile.preview,
                plottedImage: plotted_image,
                wetlandPercentage: wetland_percentage
              }
            });
          }, 2000); // wait 2 seconds to simulate processing time
        }, 1000); // short pause before switching to processing

      });
    } catch (error) {
      console.error("Upload failed:", error);
      setUploadStatus("Upload failed. Please try again.");
    }
  };

  return (
    <div className="upload-container">

      <div className="uploadbox">

        <div {...getRootProps()} className="dropzone">
          <input {...getInputProps()} />
          <p>Drop your files here</p>

          {selectedFile && (
            <div className="preview-container">
              <img src={selectedFile.preview} alt="preview" className="preview-image" />
            </div>
          )}

        </div>

      </div>

      <button className="analyze-button" onClick={handleUpload}>Analyze</button>

      <p className="status">{uploadStatus}</p>
      {showProgress && (
        <div className="progress-bar">

          <div className="progress-percent">
            {`${progress}%`}
          </div>

          <div className="progress" style={{ width: `${progress}%` }}>
          </div>

        </div>)}

    </div>
  );
};

export default FileUpload;
