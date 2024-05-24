#include <stdio.h>
#define INF 1000000

int main() {
  int n,m,i,j,k,s1,s2,d[100][100];
  scanf("%d %d", &n,&m);
  for(i=0;i<n;i++) for(j=0;j<n;j++) d[i][j]=(i==j)?0:INF;
  for(i=0;i<m;i++) {
    scanf("%d %d %d", &s1,&s2,&k);
    d[s1-1][s2-1]=d[s2-1][s1-1]=k; 
  }
  for(i=0;i<n;i++) for(j=0;j<n;j++) for(k=0;k<n;k++) {
	if(d[j][i]+d[i][k]<d[j][k]) d[j][k]=d[j][i]+d[i][k];
      }
  m=0;
  for(i=0;i<n;i++) for(j=i+1;j<n;j++) if(d[i][j]>=m) {
	s1=i+1;
	s2=j+1;
	m=d[i][j];
       //printf("%d %d %d\n", s1,s2,m);
      }
  printf("%d\n",m*100);
  return 0;
}
