#include <cstdio>
#include <algorithm>
#include <vector>
using namespace std;

int main() {
  int N, K;
  scanf("%d %d", &N, &K);
  vector<int> pos, neg;
  for (int i = 0; i < N; i++) {
    int x;
    scanf("%d", &x);
    if (x >= 0) pos.push_back(x);
    else neg.push_back(-x);
  }
  sort(pos.rbegin(), pos.rend());
  sort(neg.rbegin(), neg.rend());
  int tot = 0, farthest = 0;
  for (size_t i = 0; i < pos.size(); i += K) tot += 2 * pos[i];
  for (size_t i = 0; i < neg.size(); i += K) tot += 2 * neg[i];
  if (!pos.empty()) farthest = max(farthest, pos[0]);
  if (!neg.empty()) farthest = max(farthest, neg[0]);
  printf("%d\n", tot - farthest);
  return 0;
}
