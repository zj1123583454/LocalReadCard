#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <dlfcn.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include "wiringSerial.h"
#define Port	8080
#define BufSiz	1500
#define ENABLE		1
#define DISNABLE	0
//#define ServerIP	"221.122.60.49"
#define ServerIP	"172.16.0.185"
#define LIBNAME		"libwlt.so"
#define DEBUG

uint8_t RF_Error[5]={0x55,0x01,0x02,0x00,0xaa};
uint8_t RF_Full[7]={0x55,0x03,0x02,0x6d,0x00,0x00,0xaa};
int main(int argc,char *argv[])
//int Begin(void)
{
	int sockfp=-1;
	int serialfp=-1;	
	int FileFlag=-1;
	int Rx_Siz=0;
	int i=0;
	int Number=0;
	int Number2=0;
	int WriteFlag=-1;
	uint8_t Buffer[BufSiz]={0};
	uint8_t ImgBuffer[1024]={0};
	uint8_t test[50]={0};
	void *handle;
	int (*Unpack)(char *,char *, int);
	//打开射频模块并测试模块是否可用
	serialfp=Find_RFModule("/dev/ttyUSB0");
			if(serialfp<0)
			{
				perror("RF_Module Find\n");
			}
	sockfp=ConnectServer(ServerIP,Port);
			if(sockfp<0)
			{
				perror("Server Connect\n");
			}	
	
	write(sockfp,"StartReadCard",13);
		while(1)
		{
			Number=read(sockfp,Buffer,BufSiz);
			if(Buffer[0]==0x55 && Buffer[Number-1]==0xaa)
			{
#ifdef DEBUG
				printf("Socket read Data:");
				printarr(Buffer,Number);
				printf("Socket read count:%d\n",Number);	
#endif
				if(Number>1290)
				{
					//读卡成功会返回大于1290字节的身份证信息
					FileFlag=SaveCard(Buffer,Number);	
					if(FileFlag!=0)
					{	
						printf("Wrie Card File\n");
					}
					close(serialfp);
					close(sockfp);
					return 0;
				}

				i=write(serialfp,Buffer,Number);
#ifdef DEBUG
				printf("写入串口数据大小:%d\n本应写入数据大小:%d\n",i,Number);
				printarr(Buffer,i);
				i=0;
#endif
				//while(1)
				//{
					//Number=0;
					//Number2=0;
					//Rx_Siz=0;
					//Number=serialDataAvail(serialfp);
					//if(Number>0)
					//{
						//Number=read(serialfp,Buffer,Number);
						Number=read(serialfp,Buffer,BufSiz);
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
						else if(memcmp(Buffer,RF_Full,7)==0)
						{
							printf("Error:Full\n");
							close(sockfp);
							serialClose(serialfp);
							return -10;
							
						}
						WriteFlag=write(sockfp,Buffer,Number+Number2);
						if(WriteFlag!=Number+Number2)
						{
							printf("Socket Data Write Error\n");
							close(sockfp);
							close(serialfp);
							return -11;
						}	
					//}	
				//}
			}	
			else 
			{
				printf("Invalid Data Type \n");
				printarr(Buffer,Number);
				return -7;
			}
		Number=0;
		Number2=0;
		memset(Buffer,0,BufSiz);
	}
		
return 0;
}

