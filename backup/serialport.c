#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <wiringSerial.h>
#define Port	8080
#define BufSiz	1024
#define ENABLE		1
#define DISNABLE	0
#define ServerIP	"172.16.0.185"
#define USBtoTTL
uint8_t CloseRFCmd[3]={0x01,0x02,0x03};
uint8_t OpenRFCmd[3]={0x03,0x02,0x01};
uint8_t FindRFCmd[8]={0x55,0x04,0x01,0x01,0x01,0x01,0x00,0xaa};
uint8_t FindRFAns[8]={0x55,0x04,0x01,0x01,0x01,0x02,0x00,0xaa};
int main(int argc,char *argv[])
{
	struct sockaddr_in sockstr;
	bzero(&sockstr,sizeof(sockstr));
	int sockfp=-1;
	int serialfp=-1;	
	int Rx_Siz=0;
	int i=0;
	int Number=0;
	int WriteFlag=-1;
	uint8_t SerialFlag=DISNABLE;
	uint8_t *RetSock="Lunry_SocketType_RF";
	uint8_t Buffer[BufSiz]={0};
//	if (argc!=2) 
//	{
//		printf("参数有误\n"); 
//		return -1;
//	} 
	serialfp=serialOpen("/dev/ttyUSB0",115200);
	if (serialfp<0)	
	{
		printf("串口打开失败\n");
		return -2;
	}
	for(i=0;i<8;i++)
		serialPutchar(serialfp,FindRFCmd[i]);
	for(i=0;i<8;i++)
	{
	Buffer[i]=serialGetchar(serialfp);
	}
	if(memcmp(Buffer,FindRFAns,8)==0)
	{
	
	SerialFlag==ENABLE;
	printf("射频卡已响应\n");
	//开始Socket与Serial数据交互
	}	
	else
	{
	printf("射频模块无回应\n");
	return -5;
	}
	
	sockfp=socket(AF_INET,SOCK_STREAM,0);
	if(sockfp<0)
	{
		printf("Socket打开失败\n");
		serialClose(serialfp);
		return -3;
	}	
	sockstr.sin_family=AF_INET;
	sockstr.sin_port=htons(Port);
	inet_pton(AF_INET,ServerIP,&sockstr.sin_addr);	
	
	i=connect(sockfp,(struct sockaddr *)&sockstr,sizeof(sockstr));
	if(i==0)
	{
		printf("Socket 建立成功\n");
	}
	else
	{
		printf("Socket 连接失败\n"); 
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
				printf("服务器握手成功:%s\n",Buffer);
				
			}
			else if(memcmp(Buffer,"All_SAM_Busy",12)==0)
			{
				close(sockfp);
				close(serialfp);
				printf("安全模块繁忙:%s\n",Buffer);
				return -4;
			}
			else if(memcmp(Buffer,"Find_Idle_SAM",13)==0)
			{
				printf("Find SAM Module:%s\n",Buffer);
				write(sockfp,"StartReadCard",13);
					
			}
			else if(Buffer[0]==0x55)
			{
				printf("Socket read Data:");
				printarr(Buffer,Number);
				printf("Socket read count:%d\n",Number);
				for(i=0;i<Number;i++)
				{
					serialPutchar(serialfp,Buffer[i]);
				}
				while(1)
				{
					Number=0;
					Rx_Siz=0;
					Number=serialDataAvail(serialfp);
					if(Number>0)
					{
						for(i=0;i<Number;i++)
						{
							Buffer[i]=serialGetchar(serialfp);
						}		
						#ifdef USBtoTTL
						printf("USB to TTL Moudle\n");
						if(Number==32)
						{
							Rx_Siz=Number;
							Number=serialDataAvail(serialfp);
							printf("Serial Buffer > 32\n");
							//serialFlush(serialfp);
							for(i=0;i<Number;i++)
							{
								Buffer[32+i]=serialGetchar(serialfp);	
							}
						}
						#endif
						printf("Serial read Data:");
						printarr(Buffer,Number+Rx_Siz);
						printf("Serial read Count is :%d\n",Number+Rx_Siz);
						WriteFlag=write(sockfp,Buffer,Number+Rx_Siz);
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
				printf("不识别数据:");
				printarr(Buffer,Number);
				return -7;
			}
		}
		Number=0;
		memset(Buffer,0,BufSiz);
	}
		
		//memset(Buffer,0,BufSiz);
//		while(1)
//		{
//			//Rx_Siz=read(sockfp,Buffer,BufSiz);
//			//for(i=0;i<Rx_Siz;i++)
//			//{
//			//	serialPutchar(serialfp,Buffer[i]);		
//			//}
//			
//				
//			Number=serialDataAvail(serialfp);
//			if(Number>0)
//			{	
//				for(i=0;i<Number;i++)
//				{
//				if(i<1024)
//					Buffer[i]=serialGetchar(serialfp);
//				else
//					break;
//				}
//				write(sockfp,Buffer,i);
//				write(1,Buffer,i);
//				memset(Buffer,0,i);	
//			}
//		
//		//	Buffer[i]=serialGetchar(serialfp);
//		//	printf("%d",a);
//			//memset(Buffer,0,Rx_Siz);
//		}
return 0;
}
