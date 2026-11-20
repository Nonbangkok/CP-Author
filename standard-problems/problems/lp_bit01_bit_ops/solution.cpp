// Reference for lp_bit01_bit_ops: set / clear / toggle / test one bit with
// 1LL << k, and __builtin_popcountll for the count. O(1) per command.
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
    int type, i;
    cin >> type >> i;
    if (type == 5) {
      cout << __builtin_popcountll(a[i]) << '\n';
      continue;
    }
    int k;
    cin >> k;
    if (type == 1) a[i] |= 1LL << k;
    else if (type == 2) a[i] &= ~(1LL << k);
    else if (type == 3) a[i] ^= 1LL << k;
    else cout << ((a[i] >> k) & 1) << '\n';
  }
  for (int i = 1; i <= n; i++) cout << a[i] << (i == n ? '\n' : ' ');
}
