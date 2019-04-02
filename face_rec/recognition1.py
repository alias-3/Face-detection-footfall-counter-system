import cv2
import cv2
import numpy as np
import sqlite3
import dlib
import face_recognition
import os
import os

def rec():

	recognizer = cv2.face.LBPHFaceRecognizer_create()
	path_rec=os.path.join(os.getcwd(), 'face_rec\\recognizers\\face-trainner.yml')
	print(path_rec)
	recognizer.read(path_rec)
	cam = cv2.VideoCapture(0)
	print("scdv")
	while True:
		ret_val, img = cam.read()

	# img = cv2.flip(img, 1)
		cv2.imshow('my webcam', img)
		if cv2.waitKey(1) == 27: 
			break  # esc to quit
	cv2.destroyAllWindows()


