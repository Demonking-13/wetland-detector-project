import { useLocation, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import axios from "axios";
import "../templates/upload.css"

const UploadPage = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const file = location.state?.file;
    const [progress, setProgress] = useState(0);
    const [uploading, setUploading] = useState(true);

    useEffect(() => {
        if (!file) {
            navigate("/"); // Redirect if no file is uploaded
            return;
        }

        const uploadImage = async () => {
            const formData = new FormData();
            formData.append("image", file);

            try {
                await axios.post("http://your-api-url.com/upload", formData, {
                    headers: { "Content-Type": "multipart/form-data" },
                    onUploadProgress: (progressEvent) => {
                        const percent = Math.round((progressEvent.loaded * 100) / progressEvent.total);
                        setProgress(percent);
                    },
                });

                setUploading(false); // Upload complete
            } catch (error) {
                console.error("Upload failed:", error);
            }
        };

        uploadImage();
    }, [file, navigate]);

 
    return (
        <div className="upload-container">
            <h1>Uploading Image...</h1>

            {uploading ? (
                <div className="progress-bar">
                    <div className="progress" style={{ width: `${progress}%` }}></div>
                </div>
            ) : (
                <h2>Upload Complete!</h2>
            )}
        </div>
    );
};

export default UploadPage;
