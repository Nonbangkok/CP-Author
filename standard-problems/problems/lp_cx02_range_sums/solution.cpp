// Reference for lp_cx02_range_sums: prefix sums, pre[i] = a_1 + ... + a_i,
// each query is pre[r] - pre[l - 1], O(N + Q).
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, q;
  cin >> n >> q;
  vector<long long> pre(n + 1, 0);
  for (int i = 1; i <= n; i++) {
    long long x;
    cin >> x;
    pre[i] = pre[i - 1] + x;
  }
  while (q--) {
    int l, r;
    cin >> l >> r;
    cout << pre[r] - pre[l - 1] << '\n';
  }
}
