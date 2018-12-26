import numpy as np
import cv2 as cv
import time
import socket, select, sys, os, threading
from threading import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip, port = '192.168.43.226', 4444
s.bind((ip, port))
s.listen(10)
print("Server is Live!")

cap = cv.VideoCapture(0)

FaceCascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
EyeCascade = cv.CascadeClassifier('haarcascade_eye.xml')
check = 0
flag = False

def Alert():
    global flag, check
    if(flag):
        if(time.time() - check > 3):
            conn.send(str.encode('1'))
            print("Alert!!!!" + str(time.time() - check)[:4] + '\n')
        if(time.time() - check > 7):
            print("Informing the concerned People!! because the Eyes have not been found for more than " + str(time.time() - check)[:4] + " seconds." + '\n')
    else:
        check = time.time()

        flag = True
        


def Body():
    global flag 
    while True:
        _, frame = cap.read()
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        faces = FaceCascade.detectMultiScale(gray, 1.3, 5)      #will return x, y, width, height
        
        for (x, y, w, h) in faces:
                cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
                FaceImage = gray[y:y + h, x: x + w]
                FaceRegion = frame[y:y + h, x: x + w]
                eyes = EyeCascade.detectMultiScale(FaceImage)
                
                if(len(eyes) < 3):
                    Alert()
                else:
                    conn.send(str.encode('0'))
                    flag = False
                    for (ex, ey, ew, eh) in eyes:
                        cv.rectangle(FaceRegion, (ex + ew, ey + eh), (ex, ey),  (0, 255, 255), 2)
                

        cv.imshow('Face&Eye', frame)
        k = cv.waitKey(30) & 0xff
        if k == 27:
            break


def ClientThread(conn,addr):
      Body()
      
clients = []

while(1):
      conn, addr = s.accept()
      print('Connected with ' + addr[0])
      clients.append(conn)
      threading.Thread(target=ClientThread, args=(conn, addr)).start()
      
conn.close()
s.close()

cap.release()
cv.destroyAllWindows()
