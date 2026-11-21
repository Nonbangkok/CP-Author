// Reference for lp_dp01_frog_jumps: dp[i] = least effort to stand on stone i.
// dp[0] = 0, dp[i] = min over 1 <= d <= K of dp[i - d] + |h[i] - h[i - d]|.
// O(N K); answers reach 2 * 10^13, so long long.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, k;
  cin >> n >> k;
  vector<long long> h(n);
  for (long long &x : h) cin >> x;
  vector<long long> dp(n, LLONG_MAX);
  dp[0] = 0;
  for (int i = 1; i < n; i++)
    for (int d = 1; d <= k && i - d >= 0; d++)
      dp[i] = min(dp[i], dp[i - d] + llabs(h[i] - h[i - d]));
  cout << dp[n - 1] << '\n';
}
