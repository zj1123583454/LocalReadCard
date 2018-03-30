#!/usr/bin/evn python
#coding:utf-8
try:
	import os
	import PIL
	import cv2
	import time
	import json
	import base64	
	import serial
	import ctypes
	import numpy as np
	import Tkinter as tk
	import threading
	from GPIO import *
	from Tkinter import *
	from time import sleep
	from PIL import Image, ImageTk
	from PushResult import PushResult
	from multiprocessing import Queue
	from FaceCompare import FaceCompare
	from FaceCompare import Image_to_Base64
except ImportError as e:
	print "Import Filed",e
	exit(0)
IDPhoto="./zp/bmp"
class Gui(object):
	def __init__(self,var,CardInfo,FacecmpFlag):
		self.Width=8
		self.Height=1
		self.Color="#cccccc"
		self.Pady=12
		self.Padx=5
		self.CamWidth=480
		self.CamHeight=360
		self.max=self.CamWidth/8
		self.mini=self.CamHeight/8
		self.FaceFlag=False
		self.CompareFlag=False
		self.CardInfo=CardInfo
		self.var=var
		self.FacecmpFlag=FacecmpFlag
		self.root=Tk()

		self.windowsize="%dx%d"%(self.root.winfo_screenwidth(),self.root.winfo_screenheight())
		self.root.geometry(self.windowsize)
		self.root.title("人证核验")

		self.SrcIDImage=PIL.Image.open(r"./face/zp2.png")
		self.IDImage=ImageTk.PhotoImage(self.SrcIDImage)
		self.SrcVDImage=PIL.Image.open(r"./face/zp3.png")
		self.VDImage=ImageTk.PhotoImage(self.SrcVDImage)

		CamImage=PIL.Image.open(r"./face/camera.png")
		self.CamImage=ImageTk.PhotoImage(CamImage)

		self.Facedetect=cv2.CascadeClassifier("./LIB/haarcascade_frontalface_alt.xml")
	def Create(self):
		Xplace=0;
		Yplace=0;
		self.Name=StringVar()
		self.Sex=StringVar()
		self.Brithday=StringVar()
		self.Addr=StringVar()
		self.Number=StringVar()
		self.Result=StringVar()
		self.Info=StringVar()

		CardFrame=LabelFrame(width=200,height=300,text="证件信息")
		CardFrame.grid(row=Xplace,column=Yplace+1,pady=self.Pady,padx=self.Padx,sticky=N)

		ShowResult=Label(CardFrame,text="结果:",width=self.Width,height=self.Height,bg=self.Color)
		ShowResult.grid(row=Xplace,column=Yplace,pady=self.Pady,padx=self.Padx,sticky=W)

		ShowName=Label(CardFrame,text="姓名:",width=self.Width,height=self.Height,bg=self.Color)
		ShowName.grid(row=Xplace+1,column=Yplace,pady=self.Pady,padx=self.Padx,sticky=W)

		ShowSex=Label(CardFrame,text="性别:",width=self.Width,height=self.Height,bg=self.Color)
		ShowSex.grid(row=Xplace+2,column=Yplace,pady=self.Pady,padx=self.Padx,sticky=W)

		ShowBrithday=Label(CardFrame,text="出生日期:",width=self.Width,height=self.Height,bg=self.Color)
		ShowBrithday.grid(row=Xplace+3,pady=self.Pady,padx=self.Padx,sticky=W)

		ShowAddr=Label(CardFrame,text="家庭住址:",width=self.Width,height=self.Height,bg=self.Color)
		ShowAddr.grid(row=Xplace+5,pady=self.Pady+35,padx=self.Padx)

		ShowID=Label(CardFrame,text="身份证号:",width=self.Width,height=self.Height,bg=self.Color)
		ShowID.grid(row=Xplace+4,pady=self.Pady,padx=self.Padx,sticky=W)

		self.ResultLabel=Label(CardFrame,textvariable=self.Result,bg=self.Color,fg="red",width=self.Width+17,height=self.Height)

		self.ResultLabel.grid(row=Xplace,column=Yplace+1,pady=self.Pady,padx=self.Padx,sticky=W)
				
		self.IDName=Label(CardFrame,bg=self.Color,width=self.Width+17,height=self.Height,textvariable=self.Name)	
		self.IDName.grid(row=Xplace+1,column=Yplace+1,pady=self.Pady,padx=self.Padx,sticky=W)
		self.IDSex=Label(CardFrame,bg=self.Color,width=self.Width+17,height=self.Height,textvariable=self.Sex)
		self.IDSex.grid(row=Xplace+2,column=Yplace+1,pady=self.Pady,padx=self.Padx,sticky=W)
		self.IDBrithday=Label(CardFrame,bg=self.Color,width=self.Width+17,height=self.Height,textvariable=self.Brithday)
		self.IDBrithday.grid(row=Xplace+3,column=Yplace+1,pady=self.Pady,padx=self.Padx,sticky=W)
		self.IDAddr=Label(CardFrame,bg=self.Color,width=self.Width+33,height=self.Height,textvariable=self.Addr)
		self.IDAddr.grid(row=Xplace+5,column=Yplace+1,columnspan=2,pady=self.Pady+35,padx=self.Padx)
		self.IDNumber=Label(CardFrame,bg=self.Color,width=self.Width+17,height=self.Height,textvariable=self.Number)
		self.IDNumber.grid(row=Xplace+4,column=Yplace+1,pady=self.Pady,padx=self.Padx,sticky=W)
		self.IDFace=Label(CardFrame,bg=self.Color,width=102,height=126,image=self.IDImage,compound='center')
		self.IDFace.grid(row=Xplace,column=Yplace+1,rowspan=3,columnspan=2,pady=self.Pady,padx=self.Padx,sticky=E)

		
		VideoFrame=LabelFrame(text="人脸捕捉")
		VideoFrame.grid(row=Xplace,column=Yplace,padx=self.Padx,pady=self.Pady)

		self.VideoLabel = Label(VideoFrame,bg="#cccccc",image=self.CamImage)
		self.VideoLabel.grid()
		
		self.VidFace =Label(CardFrame,bg=self.Color,width=102,height=126,image=self.VDImage,compound='center')
		self.VidFace.grid(row=Xplace+3,column=Yplace+1,rowspan=3,columnspan=2,pady=self.Pady,padx=self.Padx,sticky=(N,E))
			
		self.Show_Text()
	def Show_Text(self):
		if not self.CardInfo.empty():
			argdict=self.CardInfo.get_nowait()
			if argdict ==None:
				self.Name.set('')
				self.Sex.set('')
				self.Brithday.set('')
				self.Addr.set('')
				self.Number.set('')

				image1=ImageTk.PhotoImage(image=self.SrcIDImage)
				self.IDFace.imgtk=image1
				self.IDFace.configure(image=image1)
		
				image2=ImageTk.PhotoImage(image=self.SrcVDImage)
				self.VidFace.imgtk=image2
				self.VidFace.configure(image=image2)
			else:
				self.Name.set(argdict['Name'])
				self.Sex.set(argdict['Sex'])
				self.Brithday.set(argdict['Bird'])
				self.Addr.set(argdict['Address'])
				self.Number.set(argdict['ID'])
				if os.path.exists("./zp.bmp"):
					img=PIL.Image.open("./zp.bmp")
					Image=ImageTk.PhotoImage(image=img)
					self.IDFace.imgtk=Image
					self.IDFace.configure(image=Image)
					self.FaceFlag=True
		if not self.var.empty():
			self.Result.set(self.var.get_nowait())
		self.IDName.after(30,self.Show_Text)
	
	def Open_Camera(self): 
		CameraNumber=CheckVideo()	
		if CameraNumber != None:
			self.cap = cv2.VideoCapture(CameraNumber)
			while not self.cap.isOpened():
				print "Camera Not Open"
				self.cap = cv2.VideoCapture(0)
				sleep(1)
			
			self.cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,self.CamWidth)
			self.cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,self.CamHeight)
			self.image=np.zeros((self.CamHeight,self.CamWidth),dtype=np.float16)
			self.Show_Video()

		else:
			print "Camera Not Found"
	def Show_Video(self):
		success,self.frame=self.cap.read()
		if not success:
			print "视频流为空!"
		self.frame=cv2.flip(self.frame,1)
		#self.frame=cv2.resize(self.frame,(240,360))
		#self.image=cv2.cvtColor(self.frame,cv2.cv.CV_BGR2GRAY)
		self.image=cv2.cvtColor(self.frame,cv2.cv.CV_RGB2BGRA)
		#cv2.equalizeHist(self.image,self.image)
		if self.FaceFlag:
			faceRects=self.Facedetect.detectMultiScale(self.image,1.2,2,
									cv2.CASCADE_SCALE_IMAGE,(self.max,self.mini))
			if len(faceRects)>0:
				x,y,w,h=faceRects[0]
				faceRect=(x,y,x+w,y+h)
				cv2.imwrite('./face/Image1.bmp',self.frame)
				self.VideoImage_Show(self.image,faceRect)
				self.FaceFlag=False
				self.FacecmpFlag.put(True)
			'''draw face frame'''
			#cv2.rectangle(self.image,(x,y),(x+w,y+h),(255,00,51))
		img=Image.fromarray(self.image)
		imgtk=ImageTk.PhotoImage(image=img)
		self.VideoLabel.imgtk=imgtk
		self.VideoLabel.configure(image=imgtk)
		self.VideoLabel.after(50,self.Show_Video)
	
	def VideoImage_Show(self,Frame,place):
		cv2.rectangle(Frame,(place[0],place[1]),(place[2],place[3]),(255,00,51),2)
		image=cv2.resize(Frame,(102,126))
		img=Image.fromarray(image)
		self.VDImage=ImageTk.PhotoImage(image=img)
		self.VidFace.imgtk=self.VDImage
		self.VidFace.configure(image=self.VDImage)
	def Mainloop(self):
		self.root.mainloop()	


def CheckVideo():
	videonum={"/dev/video0":0,"/dev/video1":1,"/dev/video2":2}
	for i in videonum:
		if os.path.exists(i):
			return videonum[i]
	return None

def EncodeData(libc,Data):
	if os.path.exists("./zp.bmp"):
		os.remove("./zp.bmp")
	
	Array=ctypes.c_char*38556 ##(102*126*3)
	Buffer=Array()
	Classify_By_Sex={'1':'男','2':'女'}
	ID_Info={}
	try:
		ID_Info["Name"]=Data[14:44].decode("utf-16").strip()#姓名
		ID_Info["Sex"]=Classify_By_Sex[Data[42:46].decode("utf-16").strip()] #性别
		ID_Info["Bird"]=Data[50:66].decode("utf-16").strip() #生日
		ID_Info["Address"]=Data[66:136].decode("utf-16").strip() #地址
		ID_Info["ID"]=Data[136:172].decode("utf-16").strip() #ID
		ID_Info["Organ"]=Data[172:202].decode("utf-16").strip() #签发机关
		ID_Info["Date"]=Data[202:256].decode("utf-16").strip() #有效日期
		if len(Data)>= 1293:
			ImageData=Data[270:270+1024]
		else:
			ImageData=Data[270:]
		if libc.unpack(ImageData,Buffer,311)!=1:
			print "Decode Imaga Failed"
			del Buffer
			return None
		else:
			del Buffer
			return ID_Info
	except:
		print "Decode data Error"
		del Buffer
		return None	
	
def GUI(var,CardInfo,PushData):
	UI=Gui(var,CardInfo,PushData)
	UI.Create()
	UI.Open_Camera()
	UI.Mainloop()

def GUI_Threading(var,CardInfo,PushData):
	p1=threading.Thread(target=GUI,args=(var,CardInfo,PushData))
	p1.setDaemon(True)
	p1.start()
	return p1

def face_compare(var,DeviceGPIO):
	value=FaceCompare()	
	lod_result=value.LoadConfig()
	if lod_result==0:
		var.put('正在导入')
		imp_result=value.Face_Import("zp")
		print imp_result
		if type(imp_result) is int:
			var.put("导入失败")
			print imp_result
			return False
		elif imp_result["status"] ==0:
			print imp_result
			var.put("导入成功")
			var.put("正在对比")
			cmp_result=value.Face_Compare("Image1")
			print cmp_result
			if cmp_result ==-1:
				var.put("网络错误")
			elif cmp_result==-2:
				var.put("请求超时")
			elif type(cmp_result) is float:
				if cmp_result < 0.4:
					var.put("未通过")
				else:
					var.put("通过")
				DeviceGPIO.BuzzingOpen()	
			print value.Face_Delete(imp_result['content']['featureId'])  #导入成功就删除
		else:
			var.put("人脸比对服务器异常")
			
		#for i in range(370,381):
		#	value.Face_Delete(i)
	else:
		var.put("配置文件错误")
		print "配置文件错误",lod_result

if __name__=="__main__":
	if os.path.exists("./zp.bmp"):
		os.remove("./zp.bmp")
	
	libc=ctypes.cdll.LoadLibrary("./LIB/libwlt.so")

	FindCard=[0xaa,0xaa,0xaa,0x96,0x69,0x00,0x03,0x20,0x01,0x22]
	SelectCard=[0xaa,0xaa,0xaa,0x96,0x69,0x00,0x03,0x20,0x02,0x21]
	ReadCard=[0xaa,0xaa,0xaa,0x96,0x69,0x00,0x03,0x30,0x01,0x32]

	var=Queue()
	CardInfo=Queue()
	FacecmpFlag=Queue()

	DeviceGPIO=GPIO()

	UI=GUI_Threading(var,CardInfo,FacecmpFlag)

	try:
		SerialHandle=serial.Serial("/dev/ttyAMA0",115200,timeout=1.1)
		flag=True
	except serial.serialutil.SerialException as e:
		print "读卡器设备错误:",e
		flag=False
	while flag:
		SerialHandle.write(FindCard)
		data=SerialHandle.read(20)
		if len(data)>11:
			SerialHandle.write(SelectCard)
			var.put("选卡")
			data=SerialHandle.read(20)
			if len(data)>11:
				SerialHandle.write(ReadCard)
				var.put("读卡")
				data=SerialHandle.read(3000)
				DataLen=len(data)
				print "数据长度",DataLen
				if DataLen>1000:
					data=EncodeData(libc,data)
					if data !=None:
						CardInfo.put(data)
						DeviceGPIO.BuzzingOpen()	
						if not FacecmpFlag.empty():
							face_compare(var,DeviceGPIO)
						else:
							continue
					else:
						continue
					#sleep(2)
				else:
					continue
			else:
				continue
		if not UI.is_alive():
			print "Programmer exit"	
			exit()
