// Naive: from every start, extend to the right with a running max/min until the
// spread exceeds D. O(N * answer), O(N^2) when long stretches are stable: must
// time out on the last subtask.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  long long d;
  cin >> n >> d;
  vector<long long> a(n);
  for (auto &v : a) cin >> v;
  int best = 0, start = 0;
  for (int l = 0; l < n; l++) {
    long long hi = a[l], lo = a[l];
    int r = l;
    while (r + 1 < n && max(hi, a[r + 1]) - min(lo, a[r + 1]) <= d) {
      r++;
      hi = max(hi, a[r]);
      lo = min(lo, a[r]);
    }
    if (r - l + 1 > best) {
      best = r - l + 1;
      start = l;
    }
  }
  cout << best << ' ' << start + 1 << '\n';
}
