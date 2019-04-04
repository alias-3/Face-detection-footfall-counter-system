import cv2
import sqlite3
import dlib
import os


def face(eid):
    
    cam = cv2.VideoCapture(0)
    detector = dlib.get_frontal_face_detector()
    #detector=cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt_tree.xml')
    #To add/update employee data
    def insertOrUpdate(Name,Id):                                            
        dbpath=os.path.join(os.getcwd(), 'face_rec\\empdata.db  ')                                      
        connect = sqlite3.connect(dbpath)                                                   #Connecting to the database
        qry = "SELECT * FROM emp WHERE Id = " + Id                            
        rows = connect.execute(qry)
        recordExist = 0
        for row in rows:                                                          #Checking wheather the id exist or not
            recordExist = 1
        if recordExist == 1:                                                      
            connect.execute("UPDATE emp SET Name = ? WHERE Id =?",(Name,Id))
        else:
        	params =(Name,Id)                                               
        	connect.execute("INSERT INTO emp(Name,Id) VALUES(?, ?)", params)
        connect.commit()                                                            #Commiting into the database
        connect.close()                                                             #Closing the connection

    #Taking input from user
    # Name = "Rathi"#    
    Id = eid 
    #input("Enter Emp Id : ")
    #Adding into database
    # insertOrUpdate(Name,Id) 

    sampleNum=0

    while(True):
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #faces = detector.detectMultiScale(gray, 1.3, 5)
        dets = detector(gray, 0)
        #for (x,y,w,h) in faces:
        for i, d in enumerate(dets): 
            #cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            cv2.rectangle(img, (d.left(), d.top()) ,(d.right(), d.bottom()),(0,255,0) ,2)
            #incrementing sample number 
            sampleNum+=1
            #saving the captured face in the dataset folder
            #cv2.imwrite("dataSet/E"+str(Id)+'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
            x=os.path.join(os.getcwd(), 'face_rec\\dataSet\\E') 
            cv2.imwrite(x+str(Id)+'.'+ str(sampleNum) + ".jpg", gray[d.top():d.bottom(), d.left():d.right()])

            cv2.imshow('Face Recording',img)
        #Wait for 100 miliseconds 
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break
        #Break if the sample number is morethan 25
        elif sampleNum>25:
            break
    cam.release()
    cv2.destroyAllWindows()
    print("Employee Added Successfully")

