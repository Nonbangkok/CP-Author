// Reference for lp_bsa01_count_range: sort once, then each query is
// upper_bound(r) - lower_bound(l), O((N + Q) log N).
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, q;
  cin >> n >> q;
  vector<int> a(n);
  for (int &x : a) cin >> x;
  sort(a.begin(), a.end());
  while (q--) {
    int l, r;
    cin >> l >> r;
    cout << upper_bound(a.begin(), a.end(), r) - lower_bound(a.begin(), a.end(), l) << '\n';
  }
}
