import pickle
import time
import urllib.request

import cv2
import numpy as np

# ------------------- INITIAL SETUP ------------------- #
# Store constants
URL = 'http://192.168.0.89:8080/shot.jpg'
RECTANGLE_COLOR = (0, 0, 255)
RECTANGLE_COLOR_UNKNOWN = (0, 0, 0)
RECTANGLE_THICKNESS = 2
FONT = cv2.FONT_HERSHEY_COMPLEX
TEXT_COLOR = (255, 255, 255)
STROKE = 1

# Fetch recognition logic
face_cascade = cv2.CascadeClassifier('src/Cascades/data/haarcascade_frontalface_alt2.xml')
side_cascade = cv2.CascadeClassifier('src/Cascades/data/haarcascade_profileface.xml')
cascades = [face_cascade, side_cascade]

recogniser = cv2.face.LBPHFaceRecognizer_create()
recogniser.read("src/trainer.yml")

# Fetch labels
labels = {}
with open("src/labels.pickle", "rb") as f:
    labels = pickle.load(f)
    labels = {value:key for key,value in labels.items()}


# ------------------- Login function ------------------- #
def login_to_server():
    # Set a password mananger
    pass_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    # Add default username and pass
    pass_mgr.add_password(None, URL, "root", "pass")
    # Set handler
    handler = urllib.request.HTTPDigestAuthHandler(pass_mgr)
    # Create opener
    opener = urllib.request.build_opener(handler)
    # Install opener
    # The password manager will now be used whenever url.request.urlopen is called
    urllib.request.install_opener(opener)
    return True

# ------------------- Function to fetch an image ------------------- #
def fetch_image():
        # Fetch image from server, and convert to array
        imgSource = urllib.request.urlopen(URL)
        imgNp = np.array(bytearray(imgSource.read()), dtype= np.uint8)
        img = cv2.imdecode(imgNp, -1)

        return img
        

# ------------------- Detect Face and display box ------------------- #
def process_image(img):
    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Fetch all images in face
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    #For each face detected
    for (x, y, w, h) in faces:
        
        width = x + w
        height = y + h
        roi_gray = gray[y:height, x:width]

        # Predict who the face belongs to, with a confidence level
        id_, conf = recogniser.predict(roi_gray)

        # If face is recognized 
        if conf >= 4 and conf <=70: 
            name = labels[id_]
            cv2.putText(img, name, (x, y), FONT, 1, TEXT_COLOR, STROKE, cv2.LINE_AA)
            cv2.rectangle(img, (x, y), (width, height), RECTANGLE_COLOR, RECTANGLE_THICKNESS)

        else: # Face is unknown
            cv2.putText(img, "UNKNOWN", (x, y), FONT, 1, TEXT_COLOR, STROKE, cv2.LINE_AA)
            cv2.rectangle(img, (x, y), (width, height), RECTANGLE_COLOR_UNKNOWN, RECTANGLE_THICKNESS)

    cv2.imshow("FaceScanner", img)


# ------------------- Main body ------------------- #

#login_to_server()

# Keep fetching images and process them 
while True:
    image = fetch_image()
    process_image(image)
    # If q is pressed, exit loop
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
