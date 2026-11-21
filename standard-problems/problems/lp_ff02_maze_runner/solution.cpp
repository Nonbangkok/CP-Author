// Reference for lp_ff02_maze_runner: BFS on the grid from S; the first time a
// cell is reached is along a shortest path. O(RC).
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int r, c;
  cin >> r >> c;
  vector<string> g(r);
  for (auto &row : g) cin >> row;
  int start = -1, goal = -1;
  for (int x = 0; x < r; x++)
    for (int y = 0; y < c; y++) {
      if (g[x][y] == 'S') start = x * c + y;
      if (g[x][y] == 'E') goal = x * c + y;
    }
  const int dr[4] = {-1, 1, 0, 0};
  const int dc[4] = {0, 0, -1, 1};
  vector<int> dist(r * c, -1);
  vector<int> q(r * c);
  int head = 0, tail = 0;
  dist[start] = 0;
  q[tail++] = start;
  while (head < tail && dist[goal] == -1) {
    int cur = q[head++];
    int x = cur / c, y = cur % c;
    for (int d = 0; d < 4; d++) {
      int nx = x + dr[d], ny = y + dc[d];
      if (nx < 0 || nx >= r || ny < 0 || ny >= c || g[nx][ny] == '#') continue;
      int nxt = nx * c + ny;
      if (dist[nxt] != -1) continue;
      dist[nxt] = dist[cur] + 1;
      q[tail++] = nxt;
    }
  }
  cout << dist[goal] << '\n';
}
