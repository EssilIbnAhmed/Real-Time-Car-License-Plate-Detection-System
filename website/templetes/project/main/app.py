
from flask import Flask, Response, render_template, request, session, redirect
from matplotlib import table
import pyrebase
import os
from datetime import datetime
import cv2
import queue
from ultralytics import YOLO
import time
from util import read_license
import threading


print(os.getcwd())
app = Flask(__name__, template_folder='templates') 

config = {
    'apiKey': "AIzaSyBPrJfhV5WNWtwU0UTTjpLppcHbg8x3TsI",
    'authDomain': "authentification-f9271.firebaseapp.com",
    'projectId': "authentification-f9271",
    'storageBucket': "authentification-f9271.appspot.com",
    'messagingSenderId': "878693826848",
    'appId': "1:878693826848:web:74a607b7d65805ee6c9745",
    'measurementId': "G-Z9VDWV55EP",
    'databaseURL': 'https://authentification-f9271-default-rtdb.europe-west1.firebasedatabase.app/'  
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app.secret_key = 'secret'

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "GET":
        return render_template('home.html')  
    if request.method == 'POST': 
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = email
            return redirect('/table')  
        except:
            return 'Failed to login'

@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/')

text_queue = queue.Queue()
@app.route('/table')
def show_table():
    carsRef = db.child('cars')
    if 'user' not in session:
        return redirect('/')
    if request.method == 'GET':
        dd = carsRef.get().val()
        data = []
        for i in dd:
            data.append({'car plate':dd[i]['car plate'],'model': dd[i]['model'], 'timestamp':datetime.utcfromtimestamp(dd[i]['timestamp']/1000.0).strftime('%Y-%m-%d %H:%M:%S UTC')})
        print(data)
    thread = threading.Thread(target=license_detection)
    thread.start()
    return render_template('table.html', data=data)

@app.route('/add_entry', methods=['POST'])
def add_entry():
    carsRef = db.child('cars')
    if 'user' not in session:
        return redirect('/')
    
    # Retrieve data from the form
    car_plate = request.form.get('car_plate')
    model = request.form.get('model')
    carsRef.push({'car plate':car_plate,'model':model, "timestamp": {".sv": "timestamp"}})

    # Here, you'd handle the addition of this data to your Firestore database
    # Use Pyrebase to interact with your Firestore database
    
    # Once data is added, you can redirect back to the table page
    return redirect('/table')

@app.route('/delete_entry', methods=['POST'])
def delete_entry():
    if 'user' not in session:
        return redirect('/')
    
    plate_to_delete = request.form.get('plate_to_delete')
    
    dd = db.child("cars").get().val()
    for i in dd:
        if dd[i]['car plate'] == plate_to_delete:
            print(dd[i]['car plate'], i)
            db.child("cars").child(i).remove()
            return redirect('/table')
        

### THE AI DETECTION CODE

def license_detection():
    model = YOLO("website/templetes/project/main/license_plate_detector.pt")
    crop_queue = queue.Queue()
    crop_saved = False

    cap = cv2.VideoCapture(0)
    def is_image_clear(img):
        blur = cv2.Laplacian(img, cv2.CV_64F).var()
        is_clear = blur > 1000
        return is_clear

    text_extraction = True
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        frame = cv2.resize(frame, (600, 350))
        results = model.predict(frame, save=False, conf=0.5, show=True, verbose=False, stream=True)
        for result in results:
            boxes = result.boxes.cpu().numpy()  # get boxes on cpu in numpy
            for box in boxes:  # iterate boxes
                r = box.xyxy[0].astype(int)
                x1, y1, x2, y2 = r
                license_plate_crop = frame[int(y1):int(y2), int(x1): int(x2), :]
                
                cv2.imshow("Result", license_plate_crop)
                cv2.moveWindow("Result", 726, 231)
                if not text_extraction and time.time() - last_extraction >= 5 :
                    text_extraction = True
                if text_extraction :
                    if is_image_clear(license_plate_crop):
                        cv2.imshow("Saved crop", license_plate_crop)
                        cv2.moveWindow("Saved crop", 726, 402)
                        try:
                            license_text = read_license(license_plate_crop)
                            print(license_text)
                            print("crop saved")
                            text_extraction= False
                            last_extraction = time.time()
                        except IndexError : 
                            print('Index Error')

if __name__ == '__main__':
    app.run(port=5500)