#include <bits/stdc++.h>

using namespace std;


struct UF {
  vector<int> e;
  UF(int n) {
    e.assign(n, -1);
  }
  bool same_set(int a, int b){ return (find(a)==find(b));}
  int size(int x) { return -e[find(x)]; }
  void join(int a, int b) {
    a = find(a); b = find(b);
    if (a == b) return;
    if (e[a] > e[b]) swap(a, b);
    e[a] += e[b]; e[b] = a;
  }
  int find(int x) {
    if (e[x] < 0) return x;
    return e[x] = find(e[x]);
  }
};

int main(){


  int n, v;
  cin >> n >> v;
  UF uf(n);
  for(int i = 0; i < v; ++i){
    int a, b, t;
    cin >> a >> b >> t;
    a--; b--;
    uf.join(a, b);
  }

  for(int i = 0; i < n; ++i){
    assert(uf.same_set(0, i));
  }
  return 42;

}
