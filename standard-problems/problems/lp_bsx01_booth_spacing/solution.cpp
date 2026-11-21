// Reference for lp_bsx01_booth_spacing: binary search on the answer d.
// ok(d) = greedy from the left can place K booths at least d apart; ok is
// true ... true false ... false, so find the last true. O(N log X).
#include <bits/stdc++.h>
using namespace std;

int n, k;
vector<long long> x;

bool ok(long long d) {
  int placed = 1;
  long long last = x[0];
  for (int i = 1; i < n && placed < k; i++)
    if (x[i] - last >= d) {
      placed++;
      last = x[i];
    }
  return placed >= k;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  cin >> n >> k;
  x.resize(n);
  for (long long &v : x) cin >> v;
  sort(x.begin(), x.end());
  long long lo = 1, hi = x[n - 1] - x[0] + 1;  // ok(lo) is true, ok(hi) is false
  while (hi - lo > 1) {
    long long mid = lo + (hi - lo) / 2;
    if (ok(mid)) lo = mid;
    else hi = mid;
  }
  cout << lo << '\n';
}
