// Naive: try every permutation of columns (one queen per row and per column),
// and only at the end check blocked cells and diagonals. O(N! * N^2): fine for
// N <= 9, far too slow for N = 12.
#include <bits/stdc++.h>
using namespace std;

int main() {
  int n;
  cin >> n;
  vector<string> board(n);
  for (auto &row : board) cin >> row;
  vector<int> col(n);
  iota(col.begin(), col.end(), 0);
  long long ways = 0;
  do {
    bool ok = true;
    for (int r = 0; r < n && ok; r++)
      if (board[r][col[r]] == '#') ok = false;
    for (int a = 0; a < n && ok; a++)
      for (int b = a + 1; b < n && ok; b++)
        if (abs(col[a] - col[b]) == b - a) ok = false;
    if (ok) ways++;
  } while (next_permutation(col.begin(), col.end()));
  cout << ways << '\n';
}
