import os
import cv2
import pickle
import numpy as np
from PIL import Image

# Fetch current directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR, "images")
SIZE = (550, 550)

face_cascade = cv2.CascadeClassifier('Cascades/data/haarcascade_frontalface_alt2.xml')
side_cascade = cv2.CascadeClassifier('Cascades/data/haarcascade_profileface.xml')
cascades = [face_cascade, side_cascade]
recogniser = cv2.face.LBPHFaceRecognizer_create()


current_id = 0
label_ids = {}
y_labels = []
x_train = []

for root, dirs, files in os.walk(image_dir):
    for file in files:
        if file.endswith("png") or file.endswith("jpg"):
            path = os.path.join(root, file)
            label = os.path.basename(root).replace(" ", "-").lower()

            if not label in label_ids:
                label_ids[label] = current_id
                current_id += 1
    
            _id = label_ids[label]
    
            #y_labels.append(label) #some number
            #x_train.append(path) # Verify this image, turn into a NUMPY array, GRAY
            pil_image = Image.open(path).convert("L") # Convert to grayscale
            final_image = pil_image.resize(SIZE, Image.ANTIALIAS)
            image_array = np.array(final_image, "uint8")

            faces = face_cascade.detectMultiScale(image_array, scaleFactor=1.1, minNeighbors=5) 
            for(x,y,w,h) in faces:
                roi = image_array[y:y+h, x:x+w]
                x_train.append(roi)
                y_labels.append(_id)
                
with open("labels.pickle", "wb") as f:
    pickle.dump(label_ids, f)

recogniser.train(x_train, np.array(y_labels))
recogniser.save("trainer.yml")