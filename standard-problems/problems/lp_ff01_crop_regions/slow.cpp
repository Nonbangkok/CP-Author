// Naive: give every cell its own label, then sweep the grid again and again,
// replacing each label by the smallest label among same-letter neighbours,
// until a whole sweep changes nothing. Correct, but a winding region needs
// one sweep per bend step: O((RC)^2) in the worst case, TLE on the last subtask.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int r, c;
  cin >> r >> c;
  vector<string> g(r);
  for (auto &row : g) cin >> row;
  vector<int> label(r * c);
  for (int i = 0; i < r * c; i++) label[i] = i;
  const int dr[4] = {-1, 1, 0, 0};
  const int dc[4] = {0, 0, -1, 1};
  bool changed = true;
  while (changed) {
    changed = false;
    for (int x = 0; x < r; x++) {
      for (int y = 0; y < c; y++) {
        int best = label[x * c + y];
        for (int d = 0; d < 4; d++) {
          int nx = x + dr[d], ny = y + dc[d];
          if (nx < 0 || nx >= r || ny < 0 || ny >= c || g[nx][ny] != g[x][y]) continue;
          best = min(best, label[nx * c + ny]);
        }
        if (best < label[x * c + y]) {
          label[x * c + y] = best;
          changed = true;
        }
      }
    }
  }
  vector<int> count(r * c, 0);
  int regions = 0, largest = 0;
  for (int i = 0; i < r * c; i++) {
    if (count[label[i]]++ == 0) regions++;
    largest = max(largest, count[label[i]]);
  }
  cout << regions << ' ' << largest << '\n';
}
