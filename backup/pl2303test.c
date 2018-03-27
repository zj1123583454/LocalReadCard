#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <dlfcn.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <wiringSerial.h>
#define Port	8080
#define BufSiz	1500
#define ENABLE		1
#define DISNABLE	0
#define ServerIP	"221.122.60.49"
//#define ServerIP	"172.16.0.185"
#define LIBNAME		"libwlt.so"
#define DEBUG
uint8_t FindRFCmd[8]={0x55,0x04,0x01,0x01,0x01,0x01,0x00,0xaa};
uint8_t FindRFAns[8]={0x55,0x04,0x01,0x01,0x01,0x02,0x00,0xaa};
uint8_t RF_Error[7]={0x55,0x01,0x02,0x00,0xaa};
int main(int argc,char *argv[])
//int Begin(void)
{
	struct sockaddr_in sockstr;
	bzero(&sockstr,sizeof(sockstr));
	int sockfp=-1;
	int serialfp=-1;	
	int IDFilefp=-1;
	int ImgFilefp=-1;
	int Rx_Siz=0;
	int i=0;
	int Number=0;
	int Number2=0;
	int WriteFlag=-1;
	uint8_t *RetSock="Lunry_SocketType_RF";
	uint8_t Buffer[BufSiz]={0};
	uint8_t ImgBuffer[1024]={0};
	uint8_t test[50]={0};
	void *handle;
	int (*Unpack)(char *,char *, int);
	
//	if (argc!=2) 
//	{
//		printf("参数有误\n"); 
//		return -1;
//	} 
	serialfp=serialOpen("/dev/ttyUSB0",115200);
	if (serialfp<0)	
	{
		printf("Open Serial Failed\n");
		return -2;
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
	}	
	else
	{
		printf("Didn't Find RF Module\n");
		return -5;
	}
	
	sockfp=socket(AF_INET,SOCK_STREAM,0);
	
	if(sockfp<0)
	{
		printf("Socket Create Failed\n");
		serialClose(serialfp);
		return -3;
	}	
	sockstr.sin_family=AF_INET;
	sockstr.sin_port=htons(Port);
	inet_pton(AF_INET,ServerIP,&sockstr.sin_addr);	
	
	i=connect(sockfp,(struct sockaddr *)&sockstr,sizeof(sockstr));
	if(i==0)
	{
		printf("Server Connect Success \n");
	}
	else
	{
		printf("Server Connect Failed \n"); 
		return -6;
	}
	while(1)
	{
		Number=read(sockfp,Buffer,BufSiz);
		if(Number>0)
		{
			
			if(memcmp(Buffer,"Lunry_AskSocketType",19)==0)
			{
				write(sockfp,"Lunry_SocketType_RF",19);
				printf("Server Message:%s\n",Buffer);
				
			}
			else if(memcmp(Buffer,"All_SAM_Busy",12)==0)
			{
				close(sockfp);
				close(serialfp);
				printf("SAM Module Busy:%s\n",Buffer);
				return -4;
			}
			else if(memcmp(Buffer,"Find_Idle_SAM",13)==0)
			{
				printf("Found SAM Module :%s\n",Buffer);
				write(sockfp,"StartReadCard",13);
					
			}
			else if(Buffer[0]==0x55)
			{
#ifdef DEBUG
				printf("Socket read Data:");
				printarr(Buffer,Number);
				printf("Socket read count:%d\n",Number);	
#endif
				if(Number>1290)
				{
					printf("Read ID Success!\n");
					if((IDFilefp=open("./IDData",O_RDWR|O_CREAT,S_IWUSR|S_IRUSR|S_IRGRP|S_IROTH))==-1)
					{
						printf("Create File Failed \n");
						close(sockfp);
						serialClose(serialfp);
						return -9;
					}		
					else 
					{
						WriteFlag=write(IDFilefp,Buffer,Number);
						//WriteFlag=write(ImgFilefp,Buffer+256,1024);					
						switch(WriteFlag)
						{
							case -1:
								printf("ID Data Write Error\n");
								break;
							case  0:
								printf("ID Data Write Failed\n");
								break;
							default:printf("ID Data Write Succese:%d\n",WriteFlag);
								close(IDFilefp);
								WriteFlag=-1;
								break;
							
						}
						//ImgFilefp=open("./ImgData",O_RDWR|O_CREAT,S_IWUSR|S_IRUSR|S_IRGRP|S_IROTH);
						//handle=dlopen(LIBNAME,RTLD_NOW);
						//Unpack=dlsym(handle,"unpack");
						//i=Unpack(Buffer+(Number-1025),ImgBuffer,311);
						//printf("Unpack value %d\n",i);
						//write(ImgFilefp,ImgBuffer,1024);	
						//dlclose(handle);
						//close(ImgFilefp);
					}		
					close(sockfp);
					serialClose(serialfp);
					return 0;
				}

					i=write(serialfp,Buffer,Number);
#ifdef DEBUG
					printf("写入串口数据大小:%d\n本应写入数据大小:%d\n",i,Number);
					printarr(Buffer,i);
					i=0;
#endif
				while(1)
				{
					Number=0;
					Number2=0;
					//Rx_Siz=0;
					Number=serialDataAvail(serialfp);
					printf("串口Buffer size is :%d",Number);
					if(Number>0)
					{
						Number=read(serialfp,Buffer,Number);
						printf("读取到:%d",Number);
						if(Number==32)
						{
							serialFlush(serialfp);
							//Number2=serialDataAvail(serialfp);
							Number2=read(serialfp,Buffer+Number,BufSiz);
						}
#ifdef DEBUG
						printf("Serial read Data:");
						printarr(Buffer,Number+Number2);
						printf("Serial read Count is :%d\n",Number+Number2);
#endif
						if(memcmp(Buffer,RF_Error,5)==0)
						{
							printf("Error:None\n");
							close(sockfp);
							serialClose(serialfp);
							return -8;
						}
						WriteFlag=write(sockfp,Buffer,Number+Number2);
						switch(WriteFlag)
						{
							case -1:
								printf("Socket Data Write Error\n");
								break;
							case  0:
								printf("Socket Data Write Failed\n");
								break;
							default:printf("Socket Data Write Succese:%d\n",WriteFlag);
								WriteFlag=-1;
								break;
							
						}	
						break;
					}	
				}
			}	
			else 
			{
				printf("Invalid Data Type \n");
				printarr(Buffer,Number);
				return -7;
			}
		}
		Number=0;
		memset(Buffer,0,BufSiz);
	}
		
return 0;
}
