// Naive O(N Q): add x to every student of [l, r] one by one, answer in O(1).
// Correct, and must time out on the last subtask.
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
    cin >> type;
    if (type == 1) {
      int l, r;
      long long x;
      cin >> l >> r >> x;
      for (int k = l; k <= r; k++) a[k] += x;
    } else {
      int i;
      cin >> i;
      cout << a[i] << '\n';
    }
  }
}
