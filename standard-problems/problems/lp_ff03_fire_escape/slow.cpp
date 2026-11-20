// Naive: simulate minute by minute. Each minute scan the whole grid twice:
// spread the fire one step, then move "every place J could be" one step into
// cells that are not walls, not burning and never visited. Correct, but
// O(RC) per minute and the escape can take ~RC/2 minutes: TLE on the last subtask.
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
  vector<char> burning(r * c, 0), here(r * c, 0), visited(r * c, 0);
  for (int x = 0; x < r; x++)
    for (int y = 0; y < c; y++) {
      if (g[x][y] == 'F') burning[x * c + y] = 1;
      if (g[x][y] == 'J') here[x * c + y] = visited[x * c + y] = 1;
    }
  for (int minute = 0;; minute++) {
    bool any = false;
    for (int x = 0; x < r; x++)
      for (int y = 0; y < c; y++) {
        if (!here[x * c + y]) continue;
        any = true;
        if (x == 0 || x == r - 1 || y == 0 || y == c - 1) {
          cout << minute + 1 << '\n';
          return 0;
        }
      }
    if (!any) break;
    vector<char> nextFire(burning), nextHere(r * c, 0);
    for (int x = 0; x < r; x++)
      for (int y = 0; y < c; y++) {
        if (g[x][y] == '#' || burning[x * c + y]) continue;
        for (int d = 0; d < 4; d++) {
          int nx = x + dr[d], ny = y + dc[d];
          if (nx >= 0 && nx < r && ny >= 0 && ny < c && burning[nx * c + ny]) {
            nextFire[x * c + y] = 1;
            break;
          }
        }
      }
    for (int x = 0; x < r; x++)
      for (int y = 0; y < c; y++) {
        int id = x * c + y;
        if (g[x][y] == '#' || visited[id] || nextFire[id]) continue;
        for (int d = 0; d < 4; d++) {
          int nx = x + dr[d], ny = y + dc[d];
          if (nx >= 0 && nx < r && ny >= 0 && ny < c && here[nx * c + ny]) {
            nextHere[id] = visited[id] = 1;
            break;
          }
        }
      }
    burning.swap(nextFire);
    here.swap(nextHere);
  }
  cout << -1 << '\n';
}
