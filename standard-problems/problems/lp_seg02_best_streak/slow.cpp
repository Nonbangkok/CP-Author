// Naive O(N Q): keep the profits in an array and run Kadane's scan over
// [l, r] for every question. Correct, and must time out on the last subtask.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, q;
  cin >> n >> q;
  vector<long long> a(n + 1);
  for (int i = 1; i <= n; i++) cin >> a[i];
  while (q--) {
    int type;
    long long x, y;
    cin >> type >> x >> y;
    if (type == 1) {
      a[x] = y;
    } else {
      long long best = a[x], ending_here = 0;
      for (int i = x; i <= y; i++) {
        ending_here = max(ending_here + a[i], a[i]);  // best streak ending at day i
        best = max(best, ending_here);
      }
      cout << best << '\n';
    }
  }
}
