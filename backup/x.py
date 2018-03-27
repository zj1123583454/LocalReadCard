#!/usr/bin/evn python
#coding:utf-8
try:
	import ctypes
	import cv2
	import time
	import numpy as np
	import multiprocessing
	from ttk import *
	import Tkinter as tk
	from Tkinter import *
	from PIL import Image, ImageTk
	import PIL
	import os
	from FaceCompare import FaceCompare
except:
	print "Import Filed"
	exit(0)

class Gui(object):
	def __init__(self,Command1,Command2):
		self.Command1=Command1
		self.Command2=Command2
		self.Sexdict={"1":"男","2":"女"}
		self.Width=8
		self.Height=1
		self.Color="#cccccc"
		self.Pady=12
		self.Padx=5
		self.root=Tk()
		self.root.geometry("760x640")
		self.root.title("人证合验")
		self.Facedetect=cv2.CascadeClassifier("./haarcascade_frontalface_alt.xml")

	def Create(self):
		self.ShowName=Label(self.root,text="姓名:",width=self.Width,height=self.Height,bg=self.Color)
		self.ShowSex=Label(self.root,text="性别:",width=self.Width,height=self.Height,bg=self.Color)
		self.ShowBrithday=Label(self.root,text="出生日期:",width=self.Width,height=self.Height,bg=self.Color)
		self.ShowAddr=Label(self.root,text="家庭住址:",width=self.Width,height=self.Height,bg=self.Color)
		self.ShowID=Label(self.root,text="身份证号:",width=self.Width,height=self.Height,bg=self.Color)
		self.VideoLabel = Label(self.root)
			
		self.Name=StringVar()
		self.Sex=StringVar()
		self.Brithday=StringVar()
		self.Addr=StringVar()
		self.Number=StringVar()
		self.Result=StringVar()
		self.Info=StringVar()
		
		self.IDName=Label(self.root,bg=self.Color,width=self.Width+17,height=self.Height,textvariable=self.Name)	
		self.IDSex=Label(self.root,bg=self.Color,width=self.Width+17,height=self.Height,textvariable=self.Sex)
		self.IDBrithday=Label(self.root,bg=self.Color,width=self.Width+17,height=self.Height,textvariable=self.Brithday)
		self.IDAddr=Label(self.root,bg=self.Color,width=self.Width+17,height=self.Height,textvariable=self.Addr)
		self.IDNumber=Label(self.root,bg=self.Color,width=self.Width+17,height=self.Height,textvariable=self.Number)
		self.IDImage=PIL.Image.open(r"./face/zp.bmp")
		self.IDImage=ImageTk.PhotoImage(self.IDImage)
		self.VDImage=PIL.Image.open(r"./face/zp.bmp")
		self.VDImage=ImageTk.PhotoImage(self.VDImage)
		
		self.IDFace=Label(self.root,bg=self.Color,width=102,height=126,image=self.IDImage,compound='center')
		self.VidFace =Label(self.root,bg=self.Color,width=102,height=126,image=self.VDImage,compound='center')

		self.CompareLabel=Label(self.root,text="比对结果:",bg=self.Color,width=self.Width+6,height=self.Height)
		self.ResultLabel=Label(self.root,textvariable=self.Result,bg=self.Color,width=self.Width+6,height=self.Height)
		#self.InfoLabel=Label(self.root,textvariable=self.Info,bg=self.Color,width=self.Width*10,height=self.Height+1)
		
		self.ReadCardbutton=Button(self.root,text="读卡",bg=self.Color,width=self.Width-3,height=self.Height,command=self.ReadCard)
		self.FaceCompare=Button(self.root,text="人脸比对",bg=self.Color,width=self.Width-3,height=self.Height,command=self.Face_Compare)
		self.FaceGrab=Button(self.root,text="抓取人脸",bg=self.Color,width=self.Width-3,height=self.Height,command=self.Image_Grab)
		self.CameraButton=Button(self.root,text="打开摄像头",bg=self.Color,width=self.Width,height=self.Height,command=self.Open_Camera)
	def Build(self):
		self.ShowName.grid(row=1,pady=self.Pady,padx=self.Padx,sticky=W)
		self.ShowSex.grid(row=2,pady=self.Pady,padx=self.Padx,sticky=W)
		self.ShowBrithday.grid(row=3,pady=self.Pady,padx=self.Padx,sticky=W)
		self.ShowAddr.grid(row=4,pady=self.Pady,padx=self.Padx,sticky=W)
		self.ShowID.grid(row=5,pady=self.Pady,padx=self.Padx,sticky=W)
		self.VideoLabel.grid(row=1,column=3,rowspan=8,columnspan=2,padx=self.Padx,pady=self.Pady,sticky=N)
		#self.VideoLabel.grid(row=1,column=3,rowspan=8,columnspan=2,padx=self.Padx*20,pady=self.Pady,sticky=N)

		self.IDName.grid(row=1,column=1,pady=self.Pady,padx=self.Padx)
		self.IDSex.grid(row=2,column=1,pady=self.Pady,padx=self.Padx)
		self.IDBrithday.grid(row=3,column=1,pady=self.Pady,padx=self.Padx)
		self.IDAddr.grid(row=4,column=1,pady=self.Pady,padx=self.Padx)
		self.IDNumber.grid(row=5,column=1,pady=self.Pady,padx=self.Padx)
		self.IDFace.grid(row=6,columnspan=2,pady=self.Pady*3,padx=self.Padx,sticky=W)
		self.VidFace.grid(row=6,columnspan=2,pady=self.Pady*3,padx=self.Padx,sticky=E)
		self.CompareLabel.grid(row=7,pady=self.Pady,padx=self.Padx)
		self.ResultLabel.grid(row=7,column=1,pady=self.Pady,padx=self.Padx,sticky=E)
		self.ReadCardbutton.grid(row=8,column=0,pady=self.Pady,padx=self.Padx)
		self.FaceCompare.grid(row=8,column=1,pady=self.Pady,padx=self.Padx)
		self.FaceGrab.grid(row=8,column=2,pady=self.Pady,padx=self.Padx,sticky=W)
		#self.InfoLabel.grid(row=0,column=1,columnspan=4,pady=self.Pady,padx=self.Padx)
		self.CameraButton.grid(row=8,column=3,pady=self.Pady,padx=self.Padx)
	def Show_Text(self):
		self.Name.set(self.CardName)
		self.Sex.set(self.CardSex)
		self.Brithday.set(self.CardBirthday)
		self.Addr.set(self.CardSite)
		self.Number.set(self.CardID)
		#self.Result.set("")

	def Card(self):
		OpenC=ctypes.cdll.LoadLibrary
		Libso=OpenC(r'./ReadCard')
		serfp=Libso.Begin()
		if serfp!=0:
			print "serfp is :",serfp
			return 0
		#print "Read File Data:"
	def Show_Info(self):
		Filefp=open(r"./IDData","r+")
		IDData=Filefp.read()
		self.CardName=IDData[17:31].decode("utf-16").strip()
		self.CardSex =IDData[41:49].decode("utf-16").strip()
		self.CardBirthday=IDData[53:69].decode("utf-16").strip()
		self.CardSite=IDData[69:135].decode("utf-16").strip()
		self.CardID=IDData[139:175].decode("utf-16").strip()
		#self.CardImg=IDData[-1022:-2]
		#print "Name:",self.CardName,"Sex:",self.CardSex,"BirthDay:",self.CardBirthday,"Address:",self.CardSite,"ID:",self.CardID
		Filefp.close()
		self.IDImage=PIL.Image.open(r"./face/zp2.bmp")
		self.IDImage=ImageTk.PhotoImage(self.IDImage)
		self.IDFace['image']=self.IDImage
		self.Show_Text()
	def Open_Camera(self):
		self.cap = cv2.VideoCapture(0)
		self.Show_Video()
		#self.Show_Text()
	def Show_Video(self):
		if not self.cap.isOpened():
			print "camera not open"
			return -1
		self.success,self.frame=self.cap.read()
		if not self.success:
			print "视频流为空!"
			exit()
		#self.frame=cv2.resize(self.frame,(380,510))
		self.frame=cv2.resize(self.frame,(336,448))
		self.frame=cv2.flip(self.frame,1)
		size=self.frame.shape[:2]
		h,w=size	
		minSize=(int(w/8),int(h/8))
		self.image=np.zeros((336,448),dtype=np.float16)
		#image=np.zeros((380,510),dtype=np.float16)
		self.image=cv2.cvtColor(self.frame,cv2.cv.CV_BGR2GRAY)
		cv2.equalizeHist(self.image,self.image)
		faceRects=self.Facedetect.detectMultiScale(self.image,1.2,2,
											cv2.CASCADE_SCALE_IMAGE,minSize)
		if len(faceRects)>0:
			print '检测到人脸'
			faceRect=faceRects[0]
			x,y,w,h=faceRect
			cv2.rectangle(self.frame,(x,y),(x+w,y+h),(255,00,51))
		img=Image.fromarray(self.frame)
		imgtk=ImageTk.PhotoImage(image=img)
		self.VideoLabel.imgtk=imgtk
		self.VideoLabel.configure(image=imgtk)
		self.VideoLabel.after(10,self.Show_Video)
	
	def Image_Grab(self):
		FaceImage=self.frame[:]
		FaceImage=cv2.resize(FaceImage,(102,126))
		cv2.imwrite('./face/Image.jpg',FaceImage)
		self.VDImage=PIL.Image.open(r"./face/Image.jpg")
		self.VDImage=ImageTk.PhotoImage(self.VDImage)
		self.VidFace['image']=self.VDImage
	
	def ReadCard(self):
		#p1=multiprocessing.Process(target=self.Card)
		#p1.start()
		self.Show_Info()
	def Face_Compare(self):
		result=FaceCompare("cl3","Image","cl3")
		if '"status":0' in result.FaceImport():
			print "Face Import Success"
			print result.Face_Compare("Image")
		else:
	
			print "人脸导入失败"

	def Mainloop(self):
		self.root.mainloop()	
def a():
	pass
def ChineseEncode(Str):
	return Str.decode("gb2312","ignore").encode("utf-8")
if __name__=="__main__":
	var=Gui(a,a)
	var.Create()
	var.Build()
	var.Mainloop()
