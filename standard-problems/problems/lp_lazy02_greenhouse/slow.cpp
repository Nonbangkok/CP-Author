// Naive O(N Q): change every bed in [l, r] one by one, and scan [l, r] for
// every question. Correct, and must time out on the last subtask.
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
    int type, l, r;
    cin >> type >> l >> r;
    if (type == 3) {
      long long best = a[l];
      for (int i = l + 1; i <= r; i++) best = max(best, a[i]);
      cout << best << '\n';
    } else {
      long long v;
      cin >> v;
      for (int i = l; i <= r; i++) {
        if (type == 1) a[i] += v;
        else a[i] = v;
      }
    }
  }
}
