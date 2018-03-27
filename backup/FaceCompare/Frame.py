from ttk import *
import Tkinter as tk
from Tkinter import *
import cv2
from PIL import Image, ImageTk
import os
import numpy as np

global last_frame                                      #creating global variable
last_frame = np.zeros((240, 380, 3), dtype=np.uint8)
global cap
cap = cv2.VideoCapture(0)

def show_vid():                                        #creating a function
    if not cap.isOpened():                             #checks for the opening of camera
        print("cant open the camera")
    flag, frame = cap.read()
    frame = cv2.flip(frame, 1)
    if flag is None:
        print "Major error!"
    elif flag:
        global last_frame
        last_frame = frame.copy()

    pic = cv2.cvtColor(last_frame, cv2.COLOR_BGR2RGB)     #we can change the display color of the frame gray,black&white here
    img = Image.fromarray(pic)
    imgtk = ImageTk.PhotoImage(image=img)
    VideoLabel.imgtk = imgtk
    VideoLabel.configure(image=imgtk)
    VideoLabel.after(10, show_vid)

if __name__ == '__main__':
    root=tk.Tk()                                     #assigning root variable for Tkinter as tk
    root.geometry("920x640")
    root.title("Sign Language Processor")            #you can give any title
    VideoLabel = tk.Label(master=root,bg="#ccddff")
    VideoLabel.grid(column=1, rowspan=2, padx=5, pady=5)
    VideoButton=Button(root,text="Open Camera",bg="#ffccdd",command=show_vid)
    VideoButton.grid(column=0,rowspan=1)	
    ReadCardbutton=Button(root,text="ReadCard",bg="#ffccdd")
    ReadCardbutton.grid(column=0,rowspan=1)
    FaceCompare=Button(root,text="FaceCompare",bg="#ffccdd")
    FaceCompare.grid(column=0,rowspan=1)
    FaceGrab=Button(root,text="FaceGrab",bg="#ffccdd")	
    FaceGrab.grid(column=0,rowspan=1)
    root.mainloop()                                  #keeps the application in an infinite loop so it works continuosly
    cap.release()
