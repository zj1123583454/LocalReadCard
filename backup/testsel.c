#include <stdio.h>
#include <stdlib.h>
#include <string.h> 
#include <unistd.h> 
#include <sys/time.h> 
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
char buf[100] ={0}; 
int i=0;
int main(int argc, char ** argv) 
{ 
	fd_set rdfds;// 
	struct sockaddr_in Sockaddr;
	struct timeval tv; //store timeout 
	int ret; // return val 
	int Serialfp=-1;
	//Serialfp=serialOpen("/dev/ttyAMA0",115200);
	//serialFlush(Serialfp);
	Serialfp=socket(AF_INET,SOCK_STREAM,0);
	if(Serialfp<0)
		perror("\nSerialfp");
	bzero(&Sockaddr,sizeof(Sockaddr));
	Sockaddr.sin_family=AF_INET;
	Sockaddr.sin_port=htons(8080);
	inet_pton(AF_INET,"172.16.0.113",&Sockaddr.sin_addr);
	connect(Serialfp,(struct sockaddr *)&Sockaddr,sizeof(Sockaddr));
	FD_ZERO(&rdfds); //clear rdfds 
	FD_SET(Serialfp, &rdfds); //add stdin handle into rdfds 
	tv.tv_sec = 2; 
	tv.tv_usec =200; 
	ret = select(Serialfp+1, &rdfds,NULL,NULL, &tv); 
	if(ret < 0) 
		perror("\nselect");
	else if(ret == 0) 
	{
		printf("\ntimeout");
		exit(0);
	}
	else 
		printf("\nret=%d", ret); 
	
	if(FD_ISSET(Serialfp,&rdfds))
	{
		i=read(Serialfp,buf,100);
	}
	printf("i is %d\n",i);
	printarr(buf,i);
	return 0; 
}
