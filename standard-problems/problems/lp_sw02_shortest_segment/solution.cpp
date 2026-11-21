// Reference for lp_sw02_shortest_segment: variable-size sliding window, O(N).
// Grow the window to the right; while it already holds at least S, record its
// length and shrink it from the left (all values are positive).
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  long long s;
  cin >> n >> s;
  vector<long long> a(n);
  for (auto &x : a) cin >> x;
  int best = INT_MAX;
  long long sum = 0;
  int l = 0;
  for (int r = 0; r < n; r++) {
    sum += a[r];
    while (sum >= s) {
      best = min(best, r - l + 1);
      sum -= a[l++];
    }
  }
  cout << (best == INT_MAX ? -1 : best) << '\n';
}
