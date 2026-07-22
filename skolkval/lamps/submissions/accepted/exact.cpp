// Compares costs in exact integer arithmetic, scaled by 100000:
// incandescent: 5 * ceil(H/1000) * 100000 + 60 * H * P
// low energy:   60 * 100000 + 11 * H * P
#include <bits/stdc++.h>
using namespace std;

int main() {
  long long h, p;
  cin >> h >> p;

  for (long long d = 1;; ++d) {
    long long H = d * h;
    long long c1 = 500000 * ((H + 999) / 1000) + 60 * H * p;
    long long c2 = 6000000 + 11 * H * p;
    if (c1 > c2) {
      cout << d << endl;
      return 0;
    }
  }
}
