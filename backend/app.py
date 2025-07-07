# Flask and CORS for backend routing and cross-origin support
from flask import Flask, request, send_file, jsonify, url_for
from flask_cors import CORS

# For image handling and numerical operations
from PIL import Image
import os
import numpy as np
import cv2

# File handling and plotting
from pathlib import Path
import matplotlib

matplotlib.use("Agg")  # Use non-GUI backend for server-side image saving
import matplotlib.pyplot as plt

# Suppress matplotlib warnings
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib.image")

# Deep learning model handling (U-Net)
import tensorflow as tf
from keras._tf_keras.keras.models import load_model
from keras._tf_keras.keras.preprocessing.image import load_img, img_to_array

# Flask app setup
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend to communicate with this backend

# Define folders for storing files
UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "results"
PLOTTED_RESULT_FOLDER = "plotedresults"

# Create folders if they don't already exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)
os.makedirs(PLOTTED_RESULT_FOLDER, exist_ok=True)

# Load the pretrained U-Net model
MODEL_PATH = "model/final_wetland_unet.h5"  # Path to your trained model
model = load_model(MODEL_PATH)

# Image size expected by the U-Net model
IMG_HEIGHT = 256
IMG_WIDTH = 256


@app.route("/", methods=["GET"])
def home():
    """
    Route: /
    Method: GET
    Purpose: Health check endpoint to ensure the Flask server is running.
    """
    return "Flask server is running with U-Net model!"


@app.route("/upload", methods=["POST"])
def upload_image():
    """
    Route: /upload
    Method: POST
    Purpose: Accepts image uploads from frontend, processes them through the U-Net model,
             calculates wetland percentage, and returns result image URLs.
    Returns:
        JSON containing the detection message, mask image URL, plotted image URL, and percentage.
    """
    # Check if an image file is included in the request
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]

    # Check if the file is valid
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Save the uploaded file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    print(f"Received upload request: {file.filename}")

    # Process the image using U-Net and get mask + overlay results
    results = detect_wetlands_with_unet(file_path)

    # Return the results as JSON
    return jsonify(
        {
            "message": "Upload and detection successful",
            "wetland_percentage": results["wetland_percentage"],
            "plotted_image": url_for(
                "get_processed_image",
                filename=results["plotted_filename"],
                _external=True,
            ),
        }
    )


@app.route("/processed/<filename>", methods=["GET"])
def get_processed_image(filename):
    """
    Route: /processed/<filename>
    Method: GET
    Purpose: Serves the mask or plotted result images to the frontend.
    Args:
        filename (str): The filename to fetch.
    Returns:
        The image file if found, or 404 JSON error.
    """
    file_path = os.path.join(RESULT_FOLDER, filename)
    if not os.path.exists(file_path):
        file_path = os.path.join(PLOTTED_RESULT_FOLDER, filename)
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404
    return send_file(file_path, mimetype="image/png",as_attachment=True)


def preprocess_image(image_path):
    """
    Preprocess the image to match the U-Net model input size and format.

    Args:
        image_path (str): Path to the original image

    Returns:
        np.ndarray: Preprocessed image with shape (1, 256, 256, 3), normalized to [0,1]
    """
    img = load_img(image_path, target_size=(IMG_HEIGHT, IMG_WIDTH))  # Resize
    img_array = img_to_array(img) / 255.0  # Normalize to [0, 1]
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    return img_array


def detect_wetlands_with_unet(image_path):
    """
    Perform wetland segmentation using the U-Net model and return visual outputs.

    Args:
        image_path (str): Path to the uploaded satellite image.

    Returns:
        dict: {
            "wetland_percentage": float,
            "mask_filename": str,
            "plotted_filename": str
        }
    """
    # Preprocess the uploaded image for model input
    image_array = preprocess_image(image_path)

    # Predict the mask using the U-Net model
    predicted_mask = model.predict(image_array)[0]  # Output shape: (256, 256, 1)

    # Threshold the predicted mask to create a binary mask
    binary_mask = (predicted_mask > 0.5).astype(
        np.uint8
    ) * 255  # Now shape: (256, 256, 1)

    # Calculate wetland coverage percentage
    wetland_pixels = np.sum(binary_mask == 255)
    total_pixels = IMG_HEIGHT * IMG_WIDTH
    wetland_percentage = (wetland_pixels / total_pixels) * 100

    # Save the binary mask image
    mask_filename = f"mask_{Path(image_path).stem}.png"
    mask_path = os.path.join(RESULT_FOLDER, mask_filename)
    cv2.imwrite(mask_path, binary_mask)

    # Create and save a plotted overlay of mask on original image
    plotted_filename = f"plotted_{Path(image_path).stem}.png"
    plotted_path = os.path.join(PLOTTED_RESULT_FOLDER, plotted_filename)
    plot_mask_overlay(image_path, binary_mask, wetland_percentage, plotted_path)

    # Return paths and percentage to the upload route
    return {
        "wetland_percentage": round(wetland_percentage, 2),
        "mask_filename": mask_filename,
        "plotted_filename": plotted_filename,
    }


def plot_mask_overlay(image_path, mask, wetland_percentage, save_path):
    """
    Overlay the predicted wetland mask on the original image and save the plot.

    Args:
        image_path (str): Path to the original image
        mask (np.ndarray): Binary mask (values 0 or 255) with shape (256, 256)
        wetland_percentage (float): Detected wetland percentage to show on the plot
        save_path (str): Path where the final plotted image will be saved
    """
    # Load and normalize the original image for plotting
    original_img = load_img(image_path,target_size=(IMG_HEIGHT,IMG_WIDTH))
    original_img = img_to_array(original_img) / 255.0

    # Normalize mask to range [0, 1] for transparency
    mask_normalized = mask.squeeze() / 255.0

    # Plot image and overlay mask
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(np.clip(original_img))  # Base image
    ax.imshow(mask_normalized, cmap='Reds', alpha=0.5)  # Red transparent overlay

    # Add wetland percentage as text
    ax.text(
        10,
        30,
        f"Wetland Area: {wetland_percentage:.2f}%",
        fontsize=14,
        color="white",
        bbox=dict(facecolor="black", alpha=0.7),
    )

    ax.axis("off")

    # Save the final plot
    plt.savefig(save_path, bbox_inches="tight", pad_inches=0.1)
    plt.close(fig)


# Entry point for running the Flask server
if __name__ == "__main__":
    app.run(debug=True, port=5000)
