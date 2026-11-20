// Reference for lp_sw03_k_flavors: variable-size sliding window with counts,
// O(N log N) for the compression and O(N) for the window. Flavours go up to
// 10^9, so they are first renumbered 0..M-1 to index a count array.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, k;
  cin >> n >> k;
  vector<int> a(n);
  for (int &x : a) cin >> x;
  vector<int> sorted_values(a);
  sort(sorted_values.begin(), sorted_values.end());
  sorted_values.erase(unique(sorted_values.begin(), sorted_values.end()), sorted_values.end());
  for (int &x : a) x = lower_bound(sorted_values.begin(), sorted_values.end(), x) - sorted_values.begin();

  vector<int> cnt(sorted_values.size(), 0);
  int distinct = 0, best = 0, l = 0;
  for (int r = 0; r < n; r++) {
    if (cnt[a[r]]++ == 0) distinct++;
    while (distinct > k) {
      if (--cnt[a[l]] == 0) distinct--;
      l++;
    }
    best = max(best, r - l + 1);
  }
  cout << best << '\n';
}
