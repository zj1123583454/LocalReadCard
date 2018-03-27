#include <stdio.h>
#include <stdlib.h>
#include <wiringPi.h>
#include <string.h>
#include <stdint.h>
#include <unistd.h>
#define BufSiz
int main()
{
	int fp=-1;
	char Buffer[BufSiz]={0};	
	uint8_t FindRFCmd[8]={0x55,0x04,0x01,0x01,0x01,0x01,0x00,0xaa};
	char size=0;
	int i=0;
	fp=serialOpen("/dev/ttyUSB0",115200);
	if(fp==-1)
	{
		printf("serial open faild");
		return -1;
	}
	size=write(fp,FindRFCmd,8);
	printf("write size is :%d\n",size);
	size=serialDataAvail(fp);
	printf("Buffer size is:%d\n",size);
	do
	{
		read(fp,ch,1);	
		
	}while(Buffer[i-1]!=0xaa);
	printf("read size is:%d\n",i);	
	printarr(Buffer,i);
return 0;
}
