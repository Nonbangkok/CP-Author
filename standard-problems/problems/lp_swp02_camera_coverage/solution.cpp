// Reference for lp_swp02_camera_coverage: one sweep over +1/-1 events,
// O(N log N). Between two consecutive event positions the number of cameras
// that see the road is constant (cur), so that gap is added to exact[cur];
// S_k is then the suffix sum exact[k] + exact[k+1] + ... + exact[N].
// Ties do not matter here: a single point has length 0. Each event is packed
// into one number 2*x + kind (kind 1 = start, 0 = end) so a plain sort is enough.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<long long> ev;
  ev.reserve(2 * n);
  for (int i = 0; i < n; i++) {
    long long l, r;
    cin >> l >> r;
    ev.push_back(2 * l + 1);
    ev.push_back(2 * r);
  }
  sort(ev.begin(), ev.end());
  vector<long long> exact(n + 2, 0);
  int cur = 0;
  for (size_t i = 0; i < ev.size(); i++) {
    if (i > 0) exact[cur] += ev[i] / 2 - ev[i - 1] / 2;
    cur += (ev[i] & 1) ? +1 : -1;
  }
  for (int k = n - 1; k >= 1; k--) exact[k] += exact[k + 1];
  for (int k = 1; k <= n; k++) cout << exact[k] << (k < n ? ' ' : '\n');
}
