#!/usr/bin/evn python
#coding:utf-8
try:
	import os
	import cv2
	import time
	import serial
	import ctypes
	from GUI import GUI_Threading
	from GPIO import *
	from time import sleep
	from PushResult import PushResult
	from multiprocessing import Queue
	from FaceCompare import FaceCompare
	from FaceCompare import Image_to_Base64
except ImportError as e:
	print "Import Filed",e
	exit(0)
IDPhoto="./zp/bmp"

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

	ID_Info["Name"] =Data[0:30].decode("utf-16").strip()#姓名
	ID_Info["Sex"]  =Classify_By_Sex[Data[30:32].decode("utf-16").strip()] #性别
	#=Data[32:36].decode("utf-16").strip()
	ID_Info["Bird"] =Data[36:52].decode("utf-16").strip() #生日
	ID_Info["Address"]=Data[52:122].decode("utf-16").strip() #地址
	ID_Info["ID"]   =Data[122:158].decode("utf-16").strip() #ID
	ID_Info["Organ"]=Data[158:188].decode("utf-16").strip() #签发机关
	ID_Info["Date"] =Data[188:256].decode("utf-16").strip() #有效日期
	if libc.unpack(Data[256:256+1024],Buffer,311)!=1:
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
	FindCard=[0xaa,0xaa,0xaa,0x96,0x69,0x00,0x03,0x20,0x01,0x22]
	SelectCard=[0xaa,0xaa,0xaa,0x96,0x69,0x00,0x03,0x20,0x02,0x21]
	ReadCard=[0xaa,0xaa,0xaa,0x96,0x69,0x00,0x03,0x30,0x01,0x32]

	var=Queue()
	CardInfo=Queue()
	FacecmpFlag=Queue()

	DeviceGPIO=GPIO()

	UI=GUI_Threading(var,CardInfo,FacecmpFlag)

	libc=ctypes.cdll.LoadLibrary("./LIB/libwlt.so")

	if os.path.exists("./zp.bmp"):
		os.remove("./zp.bmp")

	try:
		SerialHandle=serial.Serial("/dev/ttyAMA0",115200,timeout=1.2)
		flag=True
	except serial.serialutil.SerialException as e:
		print "读卡器设备错误:",e
		flag=False
	while flag:
		SerialHandle.write(FindCard)
		data=SerialHandle.read(20)
		if len(data)>11:
			var.put("选卡")
			SerialHandle.write(SelectCard)
			data=SerialHandle.read(20)
			if len(data)>11:
				var.put("读卡")
				SerialHandle.write(ReadCard)
				data=SerialHandle.read(3000)
				DataLen=len(data)
				print "数据长度",DataLen
				if DataLen==1295:
					data=data[14:]
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
					var.put("请重新放置证件")
					CardInfo.put(None)
					continue
			else:
				continue
		if not UI.is_alive():
			print "Programmer exit"	
			exit()
