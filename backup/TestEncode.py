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

def EncodeData(Data):
	libc=ctypes.cdll.LoadLibrary("./LIB/libwlt.so")
	if os.path.exists("./zp.bmp"):
		os.remove("./zp.bmp")
	Array=ctypes.c_char*38556 ##(102*126*3)
	Buffer=Array()
	Classify_By_Sex={'1':'男','2':'女'}
	ID_Info={}
	print "name",Data[14:44].decode("utf-16")#.strip()#姓名
	print "Sex",Classify_By_Sex[Data[42:46].decode("utf-16").strip()] #性别
	print "Bird",Data[50:66].decode("utf-16").strip() #生日
	print "Address",Data[66:136].decode("utf-16").strip() #地址
	print "ID",Data[136:172].decode("utf-16").strip() #ID
	print "Organ",Data[172:202].decode("utf-16").strip() #签发机关
	print "Date",Data[202:256].decode("utf-16").strip() #有效日期
	if libc.unpack(Data[270:270+1024],Buffer,311)!=1:
		print "Decode Imaga Failed"
		return None
	else:
		time.sleep(0.1)
		if os.path.exists("./zp.bmp"):
			print "Success"
			return ID_Info
		else:
			print "ImageEncode Error"
			return None
	

if __name__=="__main__":
	if os.path.exists("./zp.bmp"):
		os.remove("./zp.bmp")

	FindCard=[0xaa,0xaa,0xaa,0x96,0x69,0x00,0x03,0x20,0x01,0x22]
	SelectCard=[0xaa,0xaa,0xaa,0x96,0x69,0x00,0x03,0x20,0x02,0x21]
	ReadCard=[0xaa,0xaa,0xaa,0x96,0x69,0x00,0x03,0x30,0x01,0x32]

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
			print "选卡"
			data=SerialHandle.read(20)
			if len(data)>11:
				SerialHandle.write(ReadCard)
				print "读卡"
				data=SerialHandle.read(3000)
				DataLen=len(data)
				print "数据长度",DataLen
				if DataLen>1000:
					EncodeData(data)
					#sleep(2)
				else:
					continue
			else:
				continue
		else:
			continue
		
