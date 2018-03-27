#!/usr/bin/evn python
#coding:utf-8

try:
	import requests
	import hashlib
	import base64
	import urllib
except:
	print "Import Failed"
	exit(0)

def get_md5_value(src):
    myMd5 = hashlib.md5()
    myMd5.update(src)
    myMd5_Digest = myMd5.hexdigest()
    return myMd5_Digest

def Image_to_Base64(src):
	f=open(src,'rb') #二进制方式打开图文件
	ls_f=base64.b64encode(f.read()) #读取文件内容，转换为base64编码
	f.close()
	return ls_f 	
def Face_Compare(appExtId):
	appKey="4afcbe0fb8bf496a9e2c67931d77b349"
	url="http://119.23.148.57/face_api/faceMatch"
	headers={"content-type":"application/x-www-form-urlencoded"}
	ImageSrc=r'./face/'
	InputSrc="appExtId="+appExtId+"&appKey="+appKey+"&a753cae2fd7843f08c201848b24a13af"
	data={"appKey":appKey,"appExtId":appExtId,"minScore":"0.8","category":"1","img":Image_to_Base64(ImageSrc+appExtId+".jpg"),"sign":get_md5_value(InputSrc)}
	data=urllib.urlencode(data)
	value=requests.post(url,data,headers=headers)
	return value.text
if __name__=="__main__":
	print Face_Compare("cl1")
	
