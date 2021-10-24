#include <stdio.h>
#include <algorithm>
using namespace std;

int main() {
  int i,N,K,p,np,nn,pos[100],neg[100],tot;
  scanf("%d %d", &N, &K);
  nn=np=0;
  for(i=0;i<N;i++) {
    scanf("%d", &p);
    if(p>=0) pos[np++]=p;
    else neg[nn++]=-p;
  }
  sort(pos,pos+np);
  sort(neg,neg+nn);
  tot=-max(pos[np-1],neg[nn-1]);
  for(i=np-1;i>=0;i-=K) tot+=2*pos[i];
  for(i=nn-1;i>=0;i-=K) tot+=2*neg[i];
  printf("%d\n",tot);
  return 0;
}
