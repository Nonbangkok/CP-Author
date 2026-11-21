// Reference for lp_mono03_stable_stretch: variable sliding window with two
// monotonic deques (indices), O(N). mx keeps a decreasing run of values (front
// = window max), mn an increasing run (front = window min). For each r the
// window [l, r] is the longest stable one ending at r; recording only strict
// improvements keeps the leftmost of the longest ones.
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
  deque<int> mx, mn;
  int l = 0, best = 0, start = 0;
  for (int r = 0; r < n; r++) {
    while (!mx.empty() && a[mx.back()] <= a[r]) mx.pop_back();
    mx.push_back(r);
    while (!mn.empty() && a[mn.back()] >= a[r]) mn.pop_back();
    mn.push_back(r);
    while (a[mx.front()] - a[mn.front()] > d) {
      l++;
      if (mx.front() < l) mx.pop_front();
      if (mn.front() < l) mn.pop_front();
    }
    if (r - l + 1 > best) {
      best = r - l + 1;
      start = l;
    }
  }
  cout << best << ' ' << start + 1 << '\n';
}
