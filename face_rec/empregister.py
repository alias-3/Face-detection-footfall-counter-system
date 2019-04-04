import cv2
import numpy as np
import sqlite3
import dlib
import face_recognition
import os

def empregister(eid,ename):

    dbpath=os.path.join(os.getcwd(), 'face_rec\\empdata.db  ')                                      
    connect = sqlite3.connect(dbpath)         
    print("asdfg")
                             #Connecting to the database
    connect.execute("INSERT INTO emp(Name,Id) VALUES(?,?)",(ename,eid))
    connect.commit()
    connect.close() 
    print("chgjskd")
    return "true"