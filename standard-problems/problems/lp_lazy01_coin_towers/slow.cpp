// Naive O(N Q): add to every pile in [l, r] one by one, and add up [l, r]
// for every question. Correct, and must time out on the last subtask.
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
    if (type == 1) {
      long long v;
      cin >> v;
      for (int i = l; i <= r; i++) a[i] += v;
    } else {
      long long total = 0;
      for (int i = l; i <= r; i++) total += a[i];
      cout << total << '\n';
    }
  }
}
