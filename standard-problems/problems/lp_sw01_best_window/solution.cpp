// Reference for lp_sw01_best_window: fixed-size sliding window, O(N).
// Moving the window one step adds a[i] and removes a[i - K].
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, k;
  cin >> n >> k;
  vector<long long> a(n);
  for (auto &x : a) cin >> x;
  long long sum = 0;
  for (int i = 0; i < k; i++) sum += a[i];
  long long best = sum;
  for (int i = k; i < n; i++) {
    sum += a[i] - a[i - k];
    best = max(best, sum);
  }
  cout << best << '\n';
}
