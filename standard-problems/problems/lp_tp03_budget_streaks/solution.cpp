// Reference for lp_tp03_budget_streaks: same-direction two pointers, O(N).
// For each right end r, keep l as the smallest start whose sum still fits
// (values are non-negative, so l never moves back); then every start in
// [l, r] fits, which is r - l + 1 subarrays ending at r.
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
  long long count = 0, sum = 0;
  int l = 0;
  for (int r = 0; r < n; r++) {
    sum += a[r];
    while (sum > s) sum -= a[l++];
    count += r - l + 1;
  }
  cout << count << '\n';
}
