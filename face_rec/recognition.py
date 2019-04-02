import cv2
import numpy as np
import sqlite3
import dlib
import face_recognition
import os

def rec():
    
    recognizer = cv2.face.LBPHFaceRecognizer_create()

            
    path_rec=os.path.join(os.getcwd(), 'face_rec\\recognizers\\face-trainner.yml')
    
    recognizer.read(path_rec)
    # cascadePath = "cascades/data/haarcascade_frontalface_alt2.xml"
    # faceCascade = cv2.CascadeClassifier(cascadePath);
    detector = dlib.get_frontal_face_detector()

    def getfacename(Id):  
        dbpath=os.path.join(os.getcwd(), 'face_rec\\empdata.db  ')                                      
        connect = sqlite3.connect(dbpath)                                      #Connecting to the database
        qry = "SELECT * FROM emp WHERE Id = " + Id                            
        rows = connect.execute(qry)
        record=None
        for row in rows:                                                          #Checking wheather the id exist or not
            record = row
        connect.close() 
        return record

    #To access the webcam we pass 0
    known_face_encodings =[] 

    cam = cv2.VideoCapture(0)
    count=0
    temp=-1
    matches=[]
    while True:
        ret, img =cam.read()
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        dets = detector(img, 0)
        rgb_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        

        cv2.putText(img, str(count), (20,30), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 0, 255), 2)    

        #faces=faceCascade.detectMultiScale(gray, 1.2,5)
        #print(len(dets))
        for i, d in enumerate(dets): 

            small_frame = cv2.resize(rgb_frame, (0, 0), fx=0.25, fy=0.25)
            #rgb_small_frame = small_frame[:, :, ::-1]

            #cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            cv2.rectangle(img, (d.left(), d.top()) ,(d.right(), d.bottom()),(0,255,0) ,2)
        # for(x,y,w,h) in faces:
            # cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
            
            Id, conf = recognizer.predict(gray[d.top(): d.bottom(),d.left():d.right()])
            if conf < 75:
                profile= getfacename(str(Id))
                if profile:
                    cv2.putText(img, str(profile[0]), (d.left(),d.bottom()), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA)
                    
            else:
                cv2.putText(img, "Unknown", (d.left(),d.bottom()), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA)
                try:
                    encodings=face_recognition.face_encodings(small_frame, face_recognition.face_locations(small_frame,model="hog"))

                    for encoding in encodings:
                    
                        if(len(known_face_encodings)==0):
                            known_face_encodings.append(encoding)
                            count+=1

                        for face_encoding in known_face_encodings:
                        #print(face_encoding)
                            matches = face_recognition.compare_faces([face_encoding],encoding)
                            print(matches)
                            if (matches[0]==False): 
                                known_face_encodings.append(encoding)
                                #print(len(known_face_encodings))
                                #print(known_face_encodings)
                                count+=1

                except IndexError:
                    print("No face in scene")


        cv2.imshow('Live Cam',img) 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()