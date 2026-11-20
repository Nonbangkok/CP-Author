// Reference for lp_bsa02_nearest_value: sort once, then for each query the
// answer is lower_bound(x) or the element just before it, O((N + Q) log N).
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, q;
  cin >> n >> q;
  vector<long long> a(n);
  for (long long &v : a) cin >> v;
  sort(a.begin(), a.end());
  while (q--) {
    long long x;
    cin >> x;
    auto it = lower_bound(a.begin(), a.end(), x);  // first element >= x
    long long best;
    if (it == a.end()) best = a.back();
    else if (it == a.begin()) best = *it;
    else {
      long long below = *prev(it), above = *it;     // below < x <= above
      best = (x - below <= above - x) ? below : above;  // tie -> smaller
    }
    cout << best << '\n';
  }
}
