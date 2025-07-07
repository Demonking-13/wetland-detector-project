import React from "react";
import "../styles/result.css"
import Navbar from "../components/navbar";
import { useLocation, useNavigate } from "react-router-dom";

const Result = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const { originalImage, plottedImage, wetlandPercentage } = location.state || {};

    if (!originalImage || !plottedImage) {
        return (
            <div className="result-container">
                <Navbar />
                <div className="content">
                    <h2>Oops! No result found. Please upload an image first.</h2>
                    <button onClick={() => navigate("/")}>Go Back</button>
                </div>
            </div>
        );
    }

    const handleDownload = async () => {
        try {
            const response = await fetch(plottedImage);
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);

            const a = document.createElement("a");
            a.href = url;
            a.download = "wetland_result.png";
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url); // Clean up
        } catch (error) {
            console.error("Failed to download image:", error);
        }
    };

    return (
        <div className="result-container">
            <Navbar />
            <div className="content">

                <h1 className="heading">WETLAND DETECTION RESULT</h1>
                <p className="percentage">Wetland Area Detected: <strong>{wetlandPercentage}%</strong></p>

                <div className="images">
                    <div className="original_img">
                        <h3>Original Image</h3>
                        <img src={originalImage} alt="original" />
                    </div>

                    <div className="result_img">
                        <h3>Plotted Result</h3>
                        <img src={plottedImage} alt="plotted result" />
                    </div>
                </div>
                <button onClick={handleDownload} className="download-button">
                    Download Result
                    {/* <a href={plottedImage} download="wetland_result.png">Download Result</a> */}
                </button>
            </div>
        </div>
    );
};

export default Result;