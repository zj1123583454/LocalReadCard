#!/usr/bin/evn python
#coding:utf-8
def PushResult(PersonFace='None',Data={},Result=0.00): 	
	import json
	import requests
	import urllib
	headers={"Accept":"application/json","Content-Type":"application/json;charset=utf-8","Content-length":'200'}	
	#url="112.126.74.208"
	url="http://112.126.74.208/HumanVerification/Ver10/Face_Verification"	
	#url="http://httpbin.org/post"
	data={
	"name":Data['Name'],
	"gender":Data['Sex'],
	"nation":"GI",
	"bdate":Data['Bird'],
	"idName":11,
	"idCode":Data['ID'],
	"issueOrg":"朝阳区俊峰华庭D座709",
	"dateLimit":"2020.10.20-2080.06.06",
	"xzqh":"123456",
	"address":Data['Address'],
	"pic":Data['Face'],
	"picLen":len(Data['Face']),
	"faceImg":PersonFace,
	"faceImg1":Data['Face'],
	"faceImg2":Data['Face'],
	"compareValue":Result,
	"checkFlag":1
		}
	TxData=json.dumps(data)
	headers['Content-length']=str(len(TxData))
	value=requests.post(url=url,headers=headers,data=TxData)
	if "Error" not in value.text:
		print json.loads(value.text)
	else:
		print value.text
