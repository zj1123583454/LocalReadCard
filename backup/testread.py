#!/usr/bin/evn python
#coding:utf-8
def ReadData(FileName):
	fp=open(FileName,"r")
	data=fp.read(3000)
	fp.close()
	return data
def EncodeData(Data):
	ID_Info={}
	ID_Info["Name"]=Data[14:44].decode("utf-16").strip()#姓名
	ID_Info["Sex"]=Data[44:46].decode("utf-16").strip() #性别
	ID_Info["Bird"]=Data[50:66].decode("utf-16").strip() #生日
	ID_Info["Address"]=Data[66:136].decode("utf-16").strip() #地址
	ID_Info["ID"]=Data[136:172].decode("utf-16").strip() #ID
	ID_Info["Organ"]=Data[172:202].decode("utf-16").strip() #签发机关
	ID_Info["Date"]=Data[202:256].decode("utf-16").strip() #有效日期
	return ID_Info
	
		

if __name__=="__main__":
	data=ReadData("./IDData")
	result=EncodeData(data)
	print result
	print type(result)
	
