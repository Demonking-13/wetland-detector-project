# 🛰️ Wetland Detection from Satellite Imagery 🌿

A full-stack web application that detects and highlights wetland regions in satellite images using a U-Net deep learning model. The system enables users to upload satellite images, processes them in the backend using image segmentation techniques, and returns plotted results with analytical insights — all through a clean, responsive web interface.

---


## 🚀 Features

- 🌐 React-based frontend with drag & drop file upload
- 📦 Flask backend with U-Net model for segmentation
- 📈 Real-time upload progress bar
- 🧠 Automatic wetland detection with mask & result visualization
- 📤 Programmatic image download functionality
- 📊 Wetland coverage percentage calculation
- 🗂️ Organized result storage and access via URL

---

## 📂 Tech Stack

- **Frontend:** React, Axios, React Dropzone, React Router
- **Backend:** Flask, OpenCV, NumPy, Pillow, U-Net (Keras/TensorFlow or PyTorch)
- **Deployment (optional):** Render / Heroku / Docker

---

## 📁 Folder Structure

```

├── wetland-detector-project/
├── backend/
│ ├── model/
│ │ ├── final_wetland_unet.h5
│ │ ├── unet_training.py
│ │ ├── wetland_unet.h5
│ │ ├── train_images/
│ │ └── train_masks/
│ ├── plotedresults/
│ ├── results/
│ ├── uploads/
│ └── app.py
│
├── src/
│ ├── assets/
│ ├── components/ # FileUpload, Dropzone, etc.
│ ├── pages/ # Result.js, UploadPage.js
│ ├── styles/ # FileUpload.css, Result.css
│ ├── App.js
│ ├── index.js
│ └── ...
│
├── public/
├── package.json
└── README.md
````

---

## 🧠 How It Works

1. User uploads a satellite image via the frontend.
2. The backend receives the image, applies the U-Net segmentation model.
3. A binary wetland mask and plotted result image are generated and stored.
4. The frontend displays the results with wetland coverage percentage.
5. Users can download the result image directly.

---

## 🛠️ Setup Instructions

### 🔧 Backend (Flask)
```bash
cd backend
pip install -r requirements.txt
python app.py
````

### 🌐 Frontend (React)

```bash
cd src
npm install
npm start
```

Make sure both frontend and backend are running simultaneously. Adjust CORS and proxy as needed.

---

## 📈 Example Output

* **Original Image**
* **Detected Wetland Mask**
* **Plotted Result Image**
* **Wetland Coverage: 43.27%**

---

## 🎯 Project Objective

To create an intelligent, accessible, and automated system that analyzes satellite images and identifies wetland areas using deep learning — providing both visual overlays and statistical insight for environmental monitoring and land use assessment.

---



## 🙋‍♂️ Author

* **\Devjit Chowdury**
* 💼 [LinkedIn](https://www.linkedin.com/in/devjit-chowdhury-77bba3248)
* 📧 [Email](devjitchowdhury2003@gmail.com)

---

## 🌟 Acknowledgements

* \Kaggle Datasets for Satellite Imagery
* U-Net Architecture(https://arxiv.org/abs/1505.04597)
* OpenCV, NumPy, Flask, React contributors

