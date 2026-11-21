// Reference for lp_stl03_merge_intervals: sort the pairs by left end, then one
// sweep keeps the current strip, O(N log N).
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<pair<long long, long long>> seg(n);
  for (auto &[l, r] : seg) cin >> l >> r;
  sort(seg.begin(), seg.end());
  long long strips = 0, total = 0;
  long long curL = seg[0].first, curR = seg[0].second;
  for (int i = 1; i < n; i++) {
    if (seg[i].first <= curR) {
      curR = max(curR, seg[i].second);
    } else {
      strips++;
      total += curR - curL;
      curL = seg[i].first;
      curR = seg[i].second;
    }
  }
  strips++;
  total += curR - curL;
  cout << strips << '\n' << total << '\n';
}
