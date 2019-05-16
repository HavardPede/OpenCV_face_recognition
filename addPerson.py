import urllib.request
import numpy as np
import cv2
import time
import os.path

# ------------------- Initial setup ------------------- #

URL = 'http://192.168.0.89:8080/shot.jpg'
face_cascade = cv2.CascadeClassifier('src/Cascades/data/haarcascade_frontalface_alt2.xml')
PATH = "./src/images/"

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



# ------------------- Get name function ------------------- #
def get_name():
    nameInput = True

    while nameInput:
        print("--------------------------------------------------------")
        name = input("What is your name? ('firstname-surname')")
        print("you set your name to ", name)
        nameIsNotChecked = True
        while nameIsNotChecked:
            correct = input("is this correct? (y/n)").lower()
            if (correct == "y" or correct == "n"):
                nameIsNotChecked = False
        if correct == "y":
            nameInput = False
    return name

# ------------------- Check directory function ------------------- #
def set_directory(name):
    final_path = PATH + name + "/"
    if not os.path.exists(final_path):
        os.makedirs(final_path)
    return final_path

# ------------------- Fetch Image ------------------- #
def fetch_image():
    imgSource = urllib.request.urlopen(URL)
    imgNp = np.array(bytearray(imgSource.read()), dtype= np.uint8)
    img = cv2.imdecode(imgNp, -1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img, gray

# ------------------- Take pictures ------------------- #
def take_pictures(number_of_pictures, path):
    imageNr = 0
    while imageNr < number_of_pictures:
        #Fetch image
        img, gray = fetch_image()
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        # IFF 1 face was detected, store image
        if len(faces) == 1:
            cv2.imwrite(path + str(imageNr) + ".png", img)
            imageNr += 1
            print("image Saved: " + str(imageNr))

        cv2.imshow("Face", img)
        time.sleep(1.5)
        
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break
    return True


# ------------------- Main body ------------------- #

# login_to_server()
name = get_name()
path = set_directory(name)
if(take_pictures(10, path)):
    print("Session concluded. All images are stored")