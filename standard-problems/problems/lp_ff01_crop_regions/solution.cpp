// Reference for lp_ff01_crop_regions: flood fill (BFS with an explicit queue)
// from every cell not yet visited; neighbours are the 4 adjacent cells with the
// same letter. Each cell enters the queue once: O(RC).
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int r, c;
  cin >> r >> c;
  vector<string> g(r);
  for (auto &row : g) cin >> row;
  const int dr[4] = {-1, 1, 0, 0};
  const int dc[4] = {0, 0, -1, 1};
  vector<char> seen(r * c, 0);
  vector<int> q(r * c);
  int regions = 0, largest = 0;
  for (int sr = 0; sr < r; sr++) {
    for (int sc = 0; sc < c; sc++) {
      if (seen[sr * c + sc]) continue;
      regions++;
      char crop = g[sr][sc];
      int head = 0, tail = 0;
      seen[sr * c + sc] = 1;
      q[tail++] = sr * c + sc;
      while (head < tail) {
        int cur = q[head++];
        int x = cur / c, y = cur % c;
        for (int d = 0; d < 4; d++) {
          int nx = x + dr[d], ny = y + dc[d];
          if (nx < 0 || nx >= r || ny < 0 || ny >= c) continue;
          if (g[nx][ny] != crop || seen[nx * c + ny]) continue;
          seen[nx * c + ny] = 1;
          q[tail++] = nx * c + ny;
        }
      }
      largest = max(largest, tail);
    }
  }
  cout << regions << ' ' << largest << '\n';
}
