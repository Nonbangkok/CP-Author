// Reference for lp_dp02_secret_code: dp[i] = ways to cut the first i digits.
// dp[0] = 1; the last piece has length 1..3 (M <= 999), it may not start with
// '0' and its value must be in [1, M]: dp[i] += dp[i - len]. O(N), mod 10^9+7.
#include <bits/stdc++.h>
using namespace std;

const long long MOD = 1'000'000'007;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m;
  string s;
  cin >> n >> m >> s;
  vector<long long> dp(n + 1, 0);
  dp[0] = 1;
  for (int i = 1; i <= n; i++) {
    int value = 0, power = 1;
    for (int len = 1; len <= 3 && len <= i; len++) {
      value += (s[i - len] - '0') * power;  // piece s[i-len .. i-1]
      power *= 10;
      if (s[i - len] != '0' && value <= m) dp[i] = (dp[i] + dp[i - len]) % MOD;
    }
  }
  cout << dp[n] << '\n';
}
