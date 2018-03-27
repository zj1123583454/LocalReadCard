#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <fcntl.h>
#include <strings.h>
//#define DEBUG
void printarr(char *arr,int num)
{
	int i=0;
	for(i=0;i<num;i++)
		printf("0x%x,",arr[i]);
	printf("\n");
}
int Find_RFModule(char *device)
{
	uint8_t FindRFCmd[8]={0x55,0x04,0x01,0x01,0x01,0x01,0x00,0xaa};
	uint8_t FindRFAns[8]={0x55,0x04,0x01,0x01,0x01,0x02,0x00,0xaa};
	char i=0;
	int serialfp;
	char Buffer[10]={0};
	serialfp=serialOpen(device,115200);
	serialFlush(serialfp);
	if(serialfp<0)	
	{
		printf("Open Serial Failed\n");
		exit(serialfp);
	}
		i=write(serialfp,FindRFCmd,8);
#ifdef DEBUG
		printf("写入字节数:%d\n本应写入字节数:8\n",i);
		i=0; 
#endif
		i=read(serialfp,Buffer,8);
#ifdef DEBUG
		printf("读取到字节数:%d\n本应读取到字节数:8\n",i);
		printarr(Buffer,i);
		i=0;
#endif
	
	if(memcmp(Buffer,FindRFAns,8)==0)
	{
		printf("Found RF Module\n");
		return serialfp;
	}	
	else
	{
		printf("Didn't Find RF Module\n");
		exit(serialfp);
	}
}

int ConnectServer(char *ServerIP,int ServerPort)
{
	int sockfp=-1;
	int i=0;
	char Buffer[20]={0};
	struct sockaddr_in sockstr;
	bzero(&sockstr,sizeof(sockstr));

	sockfp=socket(AF_INET,SOCK_STREAM,0);
	if(sockfp<0)
	{
		printf("Socket Create Failed\n");
		return -1;
	}	
	sockstr.sin_family=AF_INET;
	sockstr.sin_port=htons(ServerPort);
	inet_pton(AF_INET,ServerIP,&sockstr.sin_addr);	
	
	i=connect(sockfp,(struct sockaddr *)&sockstr,sizeof(sockstr));
	if(i==0)
	{
		printf("Server Connect Success \n");
	}
	else
	{
		printf("Server Connect Failed \n"); 
		return -2;
	}
	
	read(sockfp,Buffer,20);
		
	if(memcmp(Buffer,"Lunry_AskSocketType",19)==0)
	{
		write(sockfp,"Lunry_SocketType_RF",19);
		printf("Server Message:%s\n",Buffer);
		read(sockfp,Buffer,20);	
		if(memcmp(Buffer,"All_SAM_Busy",12)==0)
		{
			close(sockfp);
			printf("SAM Module Busy:%s\n",Buffer);
			return -3;
		}
		else if(memcmp(Buffer,"Find_Idle_SAM",13)==0)
		{
			printf("Found SAM Module :%s\n",Buffer);
			return sockfp;
			//write(sockfp,"StartReadCard",13);
				
		}
	}
}
int SaveCard(char *Buffer,int FileSize)
{
	int IDFilefp=-1;
	int WriteFlag=-1;
	if((IDFilefp=open("./IDData",O_RDWR|O_CREAT,S_IWUSR|S_IRUSR|S_IRGRP|S_IROTH))==-1)
	{
		printf("Create File Failed \n");
		return -1;
	}		
	else 
	{
		WriteFlag=write(IDFilefp,Buffer,FileSize);
		sync();
		if(WriteFlag==FileSize)
		{
				printf("ID Data Write Succese:%d\n",WriteFlag);
				close(IDFilefp);
				return 0;			
		}
		else 
			return -2;
		//ImgFilefp=open("./ImgData",O_RDWR|O_CREAT,S_IWUSR|S_IRUSR|S_IRGRP|S_IROTH);
		//handle=dlopen(LIBNAME,RTLD_NOW);
		//Unpack=dlsym(handle,"unpack");
		//i=Unpack(Buffer+(Number-1025),ImgBuffer,311);
		//printf("Unpack value %d\n",i);
		//write(ImgFilefp,ImgBuffer,1024);	
		//dlclose(handle);
		//close(ImgFilefp);
	}		
}
