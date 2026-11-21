// Reference for lp_ff03_fire_escape: multi-source BFS from every 'F' gives the
// minute fire[c] each cell catches fire; then BFS from 'J' may enter cell c at
// minute t only if t < fire[c]. The first boundary cell J reaches (at minute
// t) gives the answer t + 1. O(RC).
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int r, c;
  cin >> r >> c;
  vector<string> g(r);
  for (auto &row : g) cin >> row;
  const int INF = INT_MAX;
  const int dr[4] = {-1, 1, 0, 0};
  const int dc[4] = {0, 0, -1, 1};
  vector<int> fire(r * c, INF), me(r * c, -1), q(r * c);
  int head = 0, tail = 0, start = -1;
  for (int x = 0; x < r; x++)
    for (int y = 0; y < c; y++) {
      if (g[x][y] == 'F') {
        fire[x * c + y] = 0;
        q[tail++] = x * c + y;  // every fire is a source at minute 0
      }
      if (g[x][y] == 'J') start = x * c + y;
    }
  while (head < tail) {
    int cur = q[head++];
    int x = cur / c, y = cur % c;
    for (int d = 0; d < 4; d++) {
      int nx = x + dr[d], ny = y + dc[d];
      if (nx < 0 || nx >= r || ny < 0 || ny >= c || g[nx][ny] == '#') continue;
      if (fire[nx * c + ny] != INF) continue;
      fire[nx * c + ny] = fire[cur] + 1;
      q[tail++] = nx * c + ny;
    }
  }
  head = tail = 0;
  me[start] = 0;
  q[tail++] = start;
  while (head < tail) {
    int cur = q[head++];
    int x = cur / c, y = cur % c;
    if (x == 0 || x == r - 1 || y == 0 || y == c - 1) {
      cout << me[cur] + 1 << '\n';  // step out of the grid
      return 0;
    }
    for (int d = 0; d < 4; d++) {
      int nx = x + dr[d], ny = y + dc[d];  // inside: cur is not on the boundary
      int nxt = nx * c + ny;
      if (g[nx][ny] == '#' || me[nxt] != -1 || me[cur] + 1 >= fire[nxt]) continue;
      me[nxt] = me[cur] + 1;
      q[tail++] = nxt;
    }
  }
  cout << -1 << '\n';
}
