#include "validator.h"
#include <numeric>

const int MAX_N = 700;
const int MAX_M = 2000;
const int MAX_l = 100;

struct UF {
    vector<int> p;
    UF(int n) : p(n) { iota(p.begin(), p.end(), 0); }
    int find(int x) { return p[x] == x ? x : p[x] = find(p[x]); }
    void join(int a, int b) { p[find(a)] = find(b); }
};

void run(){
	int n = Int(2, Arg("n", MAX_N));
	Endl();
	int m = Int(1, Arg("m", MAX_M));
	Endl();

	set<pair<int,int>> seen;
	UF uf(n);
	for(int i = 0; i < m; ++i){
		int a = Int(1, n);
		Space();
		int b = Int(1, n);
		Space();
		int t = Int(1, MAX_l);
		Endl();

		assert(a!=b);

		a--; b--;
		if (a>b) swap(a,b);
		assert(!seen.count({a,b}));
		seen.insert({a,b});
		uf.join(a, b);
	}

	for(int i = 0; i < n; ++i){
		assert(uf.find(0) == uf.find(i));
	}
}
