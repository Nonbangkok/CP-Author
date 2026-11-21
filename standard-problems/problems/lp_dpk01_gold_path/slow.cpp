// Naive: walk every right/down path by plain recursion and keep the best.
// There are C(R + C - 2, R - 1) paths, so it explodes on big grids: correct,
// and must time out on the last subtask. Depth <= R + C.
#include <bits/stdc++.h>
using namespace std;

int rows, cols;
vector<string> g;
int best = -1;

void walk(int r, int c, int gold) {
  if (r >= rows || c >= cols || g[r][c] == '#') return;
  gold += g[r][c] - '0';
  if (r == rows - 1 && c == cols - 1) {
    best = max(best, gold);
    return;
  }
  walk(r, c + 1, gold);
  walk(r + 1, c, gold);
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  cin >> rows >> cols;
  g.resize(rows);
  for (string &line : g) cin >> line;
  walk(0, 0, 0);
  cout << best << '\n';
}
