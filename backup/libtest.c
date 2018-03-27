#include <stdio.h>
#include <dlfcn.h>
#include <fcntl.h>
#define LIBNAME	"./libwlt.so"
int main()
{
	void *handle;
	int (*Unpack)(char *dst,char *src,int bmpSave);
	int i=0;
	int j=0;
	int fp=-1;
	int fp2=-1;
	char buffer[1500]={0};
	char buffer2[1024]={1};
	char buffer3[102*126*3]={0};
	int Number=0;
	fp=open("xp.wlt",O_RDWR);
	Number=read(fp,buffer,1500);	
	close(fp);
	fp2=open("./ImageFace",O_RDWR|O_CREAT,S_IWUSR|S_IRUSR|S_IRGRP|S_IROTH);
	printf("%d\n",fp2);
	handle=dlopen(LIBNAME,RTLD_LAZY);
	Unpack=dlsym(handle,"ZKID_PHunpack");
	i=Unpack(buffer,buffer3,310);
	printf("Unpack value %d\n",i);
	write(fp2,buffer3,Number);	
	dlclose(handle);
	close(fp2);

return 0;
}
