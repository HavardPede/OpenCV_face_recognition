# Facial Recognition with OpenCV

This project was meant as an introduction to the following:
- Python programming language
- Facial recognition 
- OpenCV

The project uses a video stream from my phone, that will be accessible through a port on the local network.
The project will access this video stream, find any face within the video stream, and try to guess who it is, based on a pretrained LBPH algorithm.


## Getting Started
#### Clone Repository
To set up the project, clone the repo to your local machine.
`git clone https://github.com/HavardPede/OpenCV_face_recognition.git`
The machine will need an installed version of the OpenCV library. This is the steps used to install OpenCV on a linux-based machine.

#### Installing OpenCV
Initially, install pip, the python package manager. This requires an installed version of python.
`sudo apt install pip `

With the pip package manager, install openCV.
`pip install opencv-python` 

#### IP webcam
With openCV set up, you will need to set up a video stream through your phone.
This is used using an application called *IP webcam* (https://play.google.com/store/apps/details?id=com.pas.webcam&hl=no). This application is easy to set up. I suggest reducing the image resolution, to increase framerate on the video stream. You will need to find what solution is best for your network speed.

**This should conclude the setup phase.**

## Running the program
#### Adding a face to the library of known faces
Initially, the facial recognition will only recognize a few of the actors from the tv-series "Game of Thrones". To view who the known faces, view the following directory:
`/"projects root-directory"/src/images`
This should show you a set of folders containing around 10 images each. The folders with the images is named according to who the images they contain depict.
To add to this collection, do the following:
1. Start a server with *IP webcam*.
2. Edit line 9 within "AddPerson.py". The ip address within the URL should reference the ip given from *IP webcam*.
3. Run AddPerson.py.
```
cd /"projects root-directory"
python addPerson.py
```
4. You will need to interact with the program through the console, to add the name of the person you want to add to the database.
5. When the video stream opens on the computer, film the person that is being added. An output within the console will let you know how many successful images has been added. It will add 10 images before terminating.
**NB! The current iteration of the project mainly focusses on frontal face features. As such, the images should mainly be on the frontal face.**

#### Training the LBPH algorithm
At any point, you may train the facial recognition algorithm on the images within "*./src/images*". To do this, run the following:
```
cd /"projects root-directory"/src/
python training.py
```
This will take a few seconds, depending on how many people are added to the training data.

#### Running the facial recognition application
1. Start a server with *IP webcam*.
2. Edit line 9 within "faceScanner.py". The ip address within the URL should reference the ip given from *IP webcam*.
3. Run faceScanner.py
```
cd /"projects root-directory"/
python faceScanner.py
```
## Future improvements
1. A wider range of cascades to recognise more angles of a face.
2. More images per person to be more accurate.
3. Converting this to an android app to show facial recognition directly on the phone.

## Author(s)
Håvard Pedersen

##Acknowledgements
This project was done by following the guide provided here:
 https://www.youtube.com/watch?v=PmZ29Vta7Vc