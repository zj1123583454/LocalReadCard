#!/usr/bin/evn python 
#coding:utf-8 
def get_md5_value(src):
	import hashlib
	myMd5 = hashlib.md5()
	myMd5.update(src)
	myMd5_Digest = myMd5.hexdigest()
	return myMd5_Digest
def Image_to_Base64(src):
	import base64
	f=open(src,'rb') 
	ls_f=base64.b64encode(f.read())
	f.close()
	return ls_f 	
def Face_Import(appExtId):
	import requests
	import urllib
	appKey="4afcbe0fb8bf496a9e2c67931d77b349"
	url="http://119.23.148.57/face_api/faceImport"
	headers={"content-type":"application/x-www-form-urlencoded"}
	ImageSrc=r'./face/'
	InputSrc="appExtId="+appExtId+"&appKey="+appKey+"&a753cae2fd7843f08c201848b24a13af"
	data={"appKey":appKey,"appExtId":appExtId,"category":"1","sign":get_md5_value(InputSrc),"img":Image_to_Base64(ImageSrc+appExtId+".jpg"),"imgType":"jpg"}
	data=urllib.urlencode(data)
	value=requests.post(url,data,headers=headers)
	return value.text
def Face_Compare(appExtId):
	import requests
	import urllib
	appKey="4afcbe0fb8bf496a9e2c67931d77b349"
	url="http://119.23.148.57/face_api/faceMatch"
	headers={"content-type":"application/x-www-form-urlencoded"}
	ImageSrc=r'./face/'
	InputSrc="appExtId="+appExtId+"&appKey="+appKey+"&a753cae2fd7843f08c201848b24a13af"
	data={"appKey":appKey,"appExtId":appExtId,"minScore":"0.8","category":"1","img":Image_to_Base64(ImageSrc+appExtId+".jpg"),"sign":get_md5_value(InputSrc)}
	data=urllib.urlencode(data)
	value=requests.post(url,data,headers=headers)
	return value.text
#if __name__=="__main__":
#	if '"status":0' in Face_Import("cl1"):
#		print "Face Import Success"
#		print Face_Compare("cl2")
#	Face_Compare("cl1")	
#	else:
#		print "Failed:"
#		
