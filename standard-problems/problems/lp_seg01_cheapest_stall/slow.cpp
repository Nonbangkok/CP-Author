// Naive O(N Q): keep the prices in an array, scan [l, r] for every question.
// Correct, and must time out on the last subtask.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, q;
  cin >> n >> q;
  vector<int> a(n + 1);
  for (int i = 1; i <= n; i++) cin >> a[i];
  while (q--) {
    int type, x, y;
    cin >> type >> x >> y;
    if (type == 1) {
      a[x] = y;
    } else {
      int best = a[x];
      for (int i = x + 1; i <= y; i++) best = min(best, a[i]);
      cout << best << '\n';
    }
  }
}
