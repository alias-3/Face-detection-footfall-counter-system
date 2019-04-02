import cv2
import numpy as np

def test():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('recognizers/face-trainner.yml')
    cascadePath = "cascades/data/haarcascade_frontalface_alt2.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath);

    #to access the webcam we pass 0
    cam = cv2.VideoCapture(0)
    while True:
        ret, im =cam.read()
        gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        faces=faceCascade.detectMultiScale(gray, 1.2,5)
        for(x,y,w,h) in faces:
            cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
            Id, conf = recognizer.predict(gray[y:y+h,x:x+w])
            if(conf<50):
                if(Id==1):
                    Id="Sarthak"
            else:
                Id="Unknown"

            cv2.putText(im, str(Id), (x,y+h), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA)  
              
            #cv2.cv.PutText(cv2.cv.fromarray(im),str(Id), (x,y+h)  font, 255)
        cv2.imshow('im',im) 
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()