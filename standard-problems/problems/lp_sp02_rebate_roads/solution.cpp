// Reference for lp_sp02_rebate_roads: Floyd-Warshall, O(N^3 + Q). Weights may be
// negative (no negative cycle), so Dijkstra is out; "unreachable" must be checked
// explicitly so that INF + (negative) is never taken as a real distance.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m, q;
  cin >> n >> m >> q;
  const long long INF = LLONG_MAX;
  vector<vector<long long>> d(n + 1, vector<long long>(n + 1, INF));
  for (int i = 1; i <= n; i++) d[i][i] = 0;
  for (int i = 0; i < m; i++) {
    int u, v;
    long long w;
    cin >> u >> v >> w;
    d[u][v] = min(d[u][v], w);
  }
  for (int k = 1; k <= n; k++)
    for (int i = 1; i <= n; i++) {
      if (d[i][k] == INF) continue;
      for (int j = 1; j <= n; j++)
        if (d[k][j] != INF && d[i][k] + d[k][j] < d[i][j]) d[i][j] = d[i][k] + d[k][j];
    }
  while (q--) {
    int a, b;
    cin >> a >> b;
    if (d[a][b] == INF) cout << "NO\n";
    else cout << d[a][b] << '\n';
  }
}
