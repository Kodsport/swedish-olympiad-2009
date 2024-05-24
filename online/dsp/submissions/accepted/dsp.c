#include <stdio.h>
#include <string.h>

int NINS=7;
char INS[7][10]={"CONST", "ADD", "SUB", "JNZ", "INPUT", "OUTPUT", "HALT"};
char PAR[7]={2,2,2,2,1,1,0};

int main() {
  int i,j,k,reg[256],p,N;
  char buf[10];
  int ins[256],par[256][2];
  scanf("%d", &N);
  for(i=0;i<N;i++) {
    scanf("%s", buf);
    for(j=0;j<NINS;j++) if(strcmp(buf,INS[j])==0) {
	ins[i]=j;
	for(k=0;k<PAR[j];k++) scanf("%d", &par[i][k]);
	break;
      }
    if(j==NINS) {printf("ERROR!\n"); return 0;}
  }
  for(i=0;i<256;i++) reg[i]=0;
  p=0;
  while(1) {
    if(ins[p]==3 && reg[par[p][0]]!=0) {p=par[p][1]; continue;}
    if(ins[p]==0) reg[par[p][1]]=par[p][0];
    if(ins[p]==1) reg[par[p][1]]+=reg[par[p][0]];
    if(ins[p]==2) reg[par[p][1]]-=reg[par[p][0]];
    if(ins[p]==4) scanf("%d", &reg[par[p][0]]);
    if(ins[p]==5) printf("%d\n", reg[par[p][0]]);
    if(ins[p]==6) return 0;
    p++;
  }    
}
