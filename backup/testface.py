#!/usr/bin/evn python
#coding:utf-8
try:
	import cv2
	from PIL import Image
	import os
except:
	print "Import Error"
	exit()

def saveFaces(image_name):
    faces = detectFaces(image_name)
    if faces:
        save_dir = image_name.split('.')[0]+"_faces"
        os.mkdir(save_dir)
        count = 0
        for (x1,y1,x2,y2) in faces:
            file_name = os.path.join(save_dir,str(count)+".jpg")
            Image.open(image_name).crop((x1,y1,x2,y2)).save(file_name)
            count+=1
def detectFaces(image_name):
    img = cv2.imread(image_name)
    face_cascade = cv2.CascadeClassifier("/home/lunry/opencv-2.4.13.3/data/haarcascades/haarcascade_frontalface_default.xml")
    if img.ndim == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img 

    faces = face_cascade.detectMultiScale(gray, 1.2, 5)
    result = []
    for (x,y,width,height) in faces:
        result.append((x,y,x+width,y+height))
    return result
if __name__=='__main__':
	saveFaces("../face/cl1.jpg")
