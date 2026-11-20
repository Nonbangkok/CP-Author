// Naive: dist[S] = 0, everything else "infinite"; sweep the whole grid again
// and again, setting dist = min(dist, neighbour + 1), until a sweep changes
// nothing. Correct, but a winding corridor needs about one sweep per step that
// goes against the sweep direction: O((RC)^2) worst case, TLE on the last subtask.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int r, c;
  cin >> r >> c;
  vector<string> g(r);
  for (auto &row : g) cin >> row;
  const int INF = INT_MAX / 2;
  vector<int> dist(r * c, INF);
  int goal = -1;
  for (int x = 0; x < r; x++)
    for (int y = 0; y < c; y++) {
      if (g[x][y] == 'S') dist[x * c + y] = 0;
      if (g[x][y] == 'E') goal = x * c + y;
    }
  const int dr[4] = {-1, 1, 0, 0};
  const int dc[4] = {0, 0, -1, 1};
  bool changed = true;
  while (changed) {
    changed = false;
    for (int x = 0; x < r; x++)
      for (int y = 0; y < c; y++) {
        if (g[x][y] == '#') continue;
        int best = dist[x * c + y];
        for (int d = 0; d < 4; d++) {
          int nx = x + dr[d], ny = y + dc[d];
          if (nx < 0 || nx >= r || ny < 0 || ny >= c || g[nx][ny] == '#') continue;
          best = min(best, dist[nx * c + ny] + 1);
        }
        if (best < dist[x * c + y]) {
          dist[x * c + y] = best;
          changed = true;
        }
      }
  }
  cout << (dist[goal] >= INF ? -1 : dist[goal]) << '\n';
}
