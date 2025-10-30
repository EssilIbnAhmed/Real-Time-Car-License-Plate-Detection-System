# Real-Time Car License Plate Detection System

This project is a real-time car license plate detection and recognition system built using Flask, YOLOv8, EasyOCR, and Firebase.  
It detects license plates from a live webcam feed, extracts their text using OCR, and stores recognized vehicle data in a Firebase database with timestamps.

---

## Features

- Real-time detection using YOLOv8  
- License plate recognition with EasyOCR  
- Firebase integration for authentication and data storage  
- Flask web interface to view, add, and delete car records  
- Dynamic table dashboard showing plate number, model, and time of detection  
- Modular design — detection, OCR, and web app components separated

---

## Web Application Overview

### 1. Authentication Page
Users must sign in before accessing the dashboard.

![Authentication Page](https://github.com/EssilIbnAhmed/Real-Time-Car-License-Plate-Detection-System/blob/main/authentication.PNG)

### 2. Dashboard Interface
The main web dashboard displays detected license plates, models, and timestamps in real time.

![Dashboard](https://github.com/EssilIbnAhmed/Real-Time-Car-License-Plate-Detection-System/blob/main/Dashboard.PNG)

### 3. Firebase Database View
All detected vehicle data is automatically stored and synchronized with Firebase Realtime Database.

![Firebase Database](https://github.com/EssilIbnAhmed/Real-Time-Car-License-Plate-Detection-System/blob/main/tab.PNG)

---

## How It Works

1. The YOLO model (`license_plate_detector.pt`) detects vehicle plates from the webcam feed.  
2. Each detected plate is cropped and passed to EasyOCR for text recognition.  
3. The recognized plate number and car model are stored in Firebase Realtime Database.  
4. The Flask app (`app.py`) displays this data in a web dashboard and allows manual entry or deletion of records.

---

## Project Structure

Real-Time-Car-License-Plate-Detection-System/
│
├── website/
│ └── templetes/project/main/
│ ├── app.py # Main Flask application
│ ├── main.py # YOLO-based live detection
│ ├── util.py # OCR utilities (EasyOCR + text formatting)
│ ├── license_plate_detector.pt # YOLO model weights
│ ├── Authentication.py # Firebase authentication setup
│ ├── static/
│ │ └── dashboard.css # Web styling
│ └── pycache/ # Cached files
│
├── README.md # Project documentation
└── .idea/ # IDE configuration (optional)

yaml
Copy code

---

## Installation and Setup

### 1. Clone the repository
```bash
git clone https://github.com/EssilIbnAhmed/Real-Time-Car-License-Plate-Detection-System.git
cd Real-Time-Car-License-Plate-Detection-System
```

### 2. Install dependencies
Make sure to have Python 3.8 or higher, then install the required libraries:

### 3. Run the application
To start the Flask web application:

```bash
Copy code
python app.py
```
To test YOLO + OCR detection directly:

```bash
Copy code
python main.py
```
Then open The browser and go to:
cpp
Copy code
http://127.0.0.1:5500/
### Example Output
When the webcam detects a car, the system highlights the license plate and extracts its text in real time.
All recognized entries appear in The Firebase dashboard and the web table.

