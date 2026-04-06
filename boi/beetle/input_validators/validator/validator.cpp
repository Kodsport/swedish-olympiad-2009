#include "validator.h"
using namespace std;


const int MAX_N = 300;
const int MAX_M = 1e6;
const int MAX_COORD = 1e4;

void run() {
    int n = Int(1, Arg("maxn", MAX_N));
    Space();
    int m = Int(1, Arg("maxm", MAX_M));
    Endl();

    set<int> seen;
    bool nonnegative = Arg("nonnegative", false);
    for (int i = 0; i < n; i++) {
        int x = Int(-MAX_COORD, MAX_COORD);
        Endl();
        if (nonnegative) {
            assert(x >= 0);
        }

        assert(!seen.count(x));
        seen.insert(x);
    }
}
