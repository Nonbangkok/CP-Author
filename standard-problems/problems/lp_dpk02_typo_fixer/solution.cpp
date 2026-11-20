// Reference for lp_dpk02_typo_fixer: weighted edit distance.
// dp[i][j] = least cost to turn A[0..i) into B[0..j):
//   dp[i][0] = i D, dp[0][j] = j I,
//   dp[i][j] = min(dp[i-1][j] + D, dp[i][j-1] + I,
//                  dp[i-1][j-1] + (A[i-1] == B[j-1] ? 0 : R)).
// Two rows are enough. O(|A| |B|) time, O(|B|) memory.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string a, b;
  int ins, del, rep;
  cin >> a >> b >> ins >> del >> rep;
  int n = a.size(), m = b.size();
  vector<int> prev(m + 1), cur(m + 1);
  for (int j = 0; j <= m; j++) prev[j] = j * ins;
  for (int i = 1; i <= n; i++) {
    cur[0] = i * del;
    for (int j = 1; j <= m; j++) {
      int keep = prev[j - 1] + (a[i - 1] == b[j - 1] ? 0 : rep);
      cur[j] = min({prev[j] + del, cur[j - 1] + ins, keep});
    }
    swap(prev, cur);
  }
  cout << prev[m] << '\n';
}
