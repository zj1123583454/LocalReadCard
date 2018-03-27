#!/usr/bin/evn python 
#coding:utf-8 
try:
	
	import requests
	import urllib
except ImportError as e:
	print "Import Error",e
	exit()

def get_md5_value(src):
	import hashlib
	myMd5 = hashlib.md5()
	myMd5.update(src)
	myMd5_Digest = myMd5.hexdigest()
	return myMd5_Digest
def Image_to_Base64(filename):
	import base64
	f=open(filename,'rb') 
	ls_f=base64.b64encode(f.read())
	f.close()
	return ls_f 	

class FaceCompare(object):
	def __init__(self):
		self.headers={"content-type":"application/x-www-form-urlencoded"}
	def LoadConfig(self):
		Handle=open("./Config/Config.cfg",'r+')
		Result=Handle.read()
		if Result=='':
			Handle.close()
			return -1
		else:
			try:
				self.Result=eval(Result)
			except:
				Handle.close()
				return -2
			Handle.close()
			self.ImageSrc=self.Result["ImageSrc"]
			self.IDImageSrc=self.Result["IDImageSrc"]
			self.AppKey=self.Result["AppKey"]
			self.AppExtId=self.Result["AppExtId"]
			self.FeatureType=self.Result["FearureType"]
			self.ImgType=self.Result["ImgType"]
			self.InputSrc="appExtId="+self.AppExtId+"&appKey="+self.AppKey+"&a753cae2fd7843f08c201848b24a13af"
			return 0
	def Face_Import(self,IDFace):
		data={
			  "appKey":self.AppKey,
			  "appExtId":self.AppExtId,
			  "featuretype":self.FeatureType,
			  "sign":get_md5_value(self.InputSrc),
			  "img":Image_to_Base64(self.IDImageSrc+IDFace+"."+self.ImgType),
			  "imgType":self.ImgType
			 }
		data=urllib.urlencode(data)
		try:
			value=requests.post(self.Result["ImportURL"],data,headers=self.headers)
		except requests.exceptions.ConnectionError:
			print "请检查网络连接"
			return -1
		if u"请求失败" in value.text:
			return -2
		elif u"未检测到人脸" in value.text:
			print "Error----------",value.text,type(value.text)
			return -3
		else:
			return eval(value.text)
	def Face_Compare(self,PersonFace):
		data={
			  "appKey":self.AppKey,
			  "appExtId":self.AppExtId,
			  "minScore":self.Result["MinScore"],
			  "featuretype":self.FeatureType,
			  "img":Image_to_Base64(self.ImageSrc+PersonFace+"."+self.ImgType),
			  "imgType":self.ImgType,
			  "sign":get_md5_value(self.InputSrc)
			 }
		data=urllib.urlencode(data)
		try:
			value=requests.post(self.Result["CompareURL"],data,headers=self.headers)
		except requests.exceptions.ConnectionError:
			print "请检查网络连接"
			return -1
		if u"请求超时" in value.text:
			print value.text
			return -2
		else:
			value=eval(value.text)
			print "比对:",value
			return round(value['content']['result'][0]['score'],2)
	def Face_Delete(self,featureId):
		featureId=str(featureId)
		data={"appKey":self.AppKey,
				"featureId":featureId,
				"sign":get_md5_value("featureId="+featureId+"&appKey="+self.AppKey+"&a753cae2fd7843f08c201848b24a13af")
				}
		data=urllib.urlencode(data)
		try:
			value=requests.post(self.Result["DeleteURL"],data,headers=self.headers)
		except requests.exceptions.ConnectionError:
			print "请检查网络连接"
			return -1
		except:
			return -2
		value=eval(value.text)
		if value["status"]==0 and value["msg"]=="success":
			return 0
		else:
			return -3
#if __name__=="__main__":
#	value=FaceCompare()	
#	if value.LoadConfig()==0:
#		result=value.Face_Import("zp")
#		print "导入:",result
#		if result <0:
#			print result
#			exit()
#		elif result["status"] ==0:
#			print value.Face_Compare("Image1")
#			print value.Face_Delete(result['content']['featureId'])
#		#for i in range(2000,2203):
#		#	value.Face_Delete(i)
