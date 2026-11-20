// Reference for lp_ss02_blocked_queens: backtracking row by row; a queen is
// placed only on a free cell whose column and both diagonals are still unused,
// so a dead branch is cut the moment it appears.
#include <bits/stdc++.h>
using namespace std;

int n;
vector<string> board;
bool usedCol[12], usedDiag1[23], usedDiag2[23];  // diag1: r + c, diag2: r - c + n - 1

long long place(int r) {
  if (r == n) return 1;
  long long ways = 0;
  for (int c = 0; c < n; c++) {
    if (board[r][c] == '#' || usedCol[c] || usedDiag1[r + c] || usedDiag2[r - c + n - 1]) continue;
    usedCol[c] = usedDiag1[r + c] = usedDiag2[r - c + n - 1] = true;
    ways += place(r + 1);
    usedCol[c] = usedDiag1[r + c] = usedDiag2[r - c + n - 1] = false;
  }
  return ways;
}

int main() {
  cin >> n;
  board.resize(n);
  for (auto &row : board) cin >> row;
  cout << place(0) << '\n';
}
