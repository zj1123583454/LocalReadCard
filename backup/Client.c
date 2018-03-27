#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <dlfcn.h>
#include <sys/socket.h>
#include <netinet/in.h>
#define Port	8080
#define BufSiz	65535
//#define ServerIP	"221.122.60.49"
#define ServerIP	"172.16.0.185"
//#define DEBUG

uint8_t RF_Error[5]={0x55,0x01,0x02,0x00,0xaa};
uint8_t RF_FindCard[8]={0x55,0x04,0x02,0x05,0x00,0x00,0x00,0xaa};
uint8_t RF_Full[7]={0x55,0x03,0x02,0x6d,0x00,0x00,0xaa};
int main(int argc,char *argv[])
{
	int sockfp=-1;
	int serialfp=-1;	
	int FileFlag=-1;
	int i=0;
	unsigned int count=0;
	unsigned int Number=0;
	unsigned int Number2=0;
	unsigned int All_Data=0;	
	int WriteFlag=-1;
	uint8_t Buffer[BufSiz]={0};
	serialfp=Find_RFModule("/dev/ttyUSB0");
	while(1)
		{
			write(serialfp,RF_FindCard,8);
			i=read(serialfp,Buffer,BufSiz);
			if(Buffer[0]==0x55 && Buffer[i-1]==0xaa)
			{
				if(memcmp(Buffer,RF_Error,i)!=0 && memcmp(Buffer,RF_Full,i)!=0)
				{
#ifdef DEBUG
					printf("Find Card\n");
#endif
					sockfp=ConnectServer(ServerIP,Port);
					if(sockfp<0)
					{
						perror("Server Connect Error\n");
					}	
					i=write(sockfp,"StartReadCard_A",15);
#ifdef DEBUG
					printf("\nReading  Card\n");
#endif
					while(1)
					{
						Number=read(sockfp,Buffer,BufSiz);
						if(Number>100)
						{
							All_Data=Buffer[1]*256+Buffer[2];
							printf("\nAll Data: %d\n",All_Data);
							count=Number;
							while((count-6)!=All_Data)
							{
								Number=read(sockfp,Buffer+count,BufSiz);
								count+=Number;
							}
							FileFlag=SaveCard(Buffer+4,count-6);	
							if(FileFlag>0)
							{	
							printf("Wrie Card File\n");
							}
							close(sockfp);
							count=0;
							All_Data=0;
							break;
								//return 0;
						} //end if(Number>1209)

						else if(Buffer[0]==0x55 && Buffer[Number-1]==0xaa)
						{
#ifdef DEBUG
								printf("Socket read Data:");
								printarr(Buffer,Number);
								printf("Socket read count:%d\n",Number);	
#endif
						
						i=write(serialfp,Buffer,Number);
#ifdef DEBUG
						printf("写入串口数据大小:%d\n本应写入数据大小:%d\n",i,Number);
						printarr(Buffer,i);
						i=0;
#endif
						Number=read(serialfp,Buffer,BufSiz);
						if(Number==32)
						{
								serialFlush(serialfp);
								Number2=read(serialfp,Buffer+Number,BufSiz);
						}//end if(Number>32)
#ifdef DEBUG
						printf("Serial read Data:");
						printarr(Buffer,Number+Number2);
						printf("Serial read Count is :%d\n",Number+Number2);
#endif
						if(memcmp(Buffer,RF_Error,5)==0)
						{
								printf("Error:None\n");
								close(sockfp);
								break;
								//serialClose(serialfp);
								//return -8;
					
						}
						else if(memcmp(Buffer,RF_Full,7)==0)
						{
								printf("Error:Full\n");
								close(sockfp);
								break;
								//serialClose(serialfp);
								//return -10;
							
						}
						WriteFlag=write(sockfp,Buffer,Number+Number2);
						if(WriteFlag!=Number+Number2)
						{
								printf("Socket Data Write Error\n");
								close(sockfp);
								break;
								//close(serialfp);
								//return -11;
						}	
					}//end if	
					else 
					{
							printf("Invalid Data Type \n");
							printarr(Buffer,Number);
							close(sockfp);
							break;
							//return -7;
					}
					Number=0;
					Number2=0;
					memset(Buffer,0,BufSiz);
				}//end while()

			}

		}
memset(Buffer,0,BufSiz);
sleep(2);
	}
			
return 0;
}

