// Reference for lp_dpk01_gold_path: dp[r][c] = most gold on a path from
// (0, 0) to (r, c), or -1 if (r, c) cannot be reached (a rock, or both the
// cell above and the cell to the left are unreachable). O(R C).
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int rows, cols;
  cin >> rows >> cols;
  vector<string> g(rows);
  for (string &line : g) cin >> line;
  vector<vector<int>> dp(rows, vector<int>(cols, -1));
  for (int r = 0; r < rows; r++)
    for (int c = 0; c < cols; c++) {
      if (g[r][c] == '#') continue;
      int from = (r == 0 && c == 0) ? 0 : -1;
      if (r > 0) from = max(from, dp[r - 1][c]);
      if (c > 0) from = max(from, dp[r][c - 1]);
      if (from >= 0) dp[r][c] = from + (g[r][c] - '0');
    }
  cout << dp[rows - 1][cols - 1] << '\n';
}
