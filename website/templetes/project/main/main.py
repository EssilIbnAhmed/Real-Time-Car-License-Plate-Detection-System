from ultralytics import YOLO
import cv2
import queue
from util import read_license
import time

model = YOLO("license_plate_detector.pt")
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
    results = model.predict(frame, save=False, conf=0.5, show=True, verbose=False, stream=True)
    for result in results:
        boxes = result.boxes.cpu().numpy()  # get boxes on cpu in numpy
        for box in boxes:  # iterate boxes
            r = box.xyxy[0].astype(int)
            x1, y1, x2, y2 = r
            license_plate_crop = frame[int(y1):int(y2), int(x1): int(x2), :]
            license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
            _, license_plate_crop_thresh = cv2.threshold(license_plate_crop_gray, 90, 255, cv2.THRESH_BINARY_INV)
            cv2.imshow("Result", license_plate_crop)
            if not text_extraction and time.time() - last_extraction >= 5 :
                text_extraction = True
            if text_extraction :
                if is_image_clear(license_plate_crop):
                    cv2.imshow("Saved crop", license_plate_crop)
                    try:
                        license_text = read_license(license_plate_crop)
                        print(license_text)
                        print("crop saved")
                        text_extraction= False
                        last_extraction = time.time()
                    except IndexError : 
                        print('Index Error')
    

