// Reference for lp_gph02_one_way_flights: one BFS from city 1 over the directed
// edges gives the fewest flights to every city at once; answer each query by
// lookup. O(N + M + Q).
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m, q;
  cin >> n >> m >> q;
  vector<vector<int>> adj(n + 1);
  for (int i = 0; i < m; i++) {
    int a, b;
    cin >> a >> b;
    adj[a].push_back(b);  // one way only
  }
  vector<int> dist(n + 1, -1);
  queue<int> bfs;
  dist[1] = 0;
  bfs.push(1);
  while (!bfs.empty()) {
    int u = bfs.front();
    bfs.pop();
    for (int v : adj[u]) {
      if (dist[v] == -1) {
        dist[v] = dist[u] + 1;
        bfs.push(v);
      }
    }
  }
  string out;
  for (int i = 0; i < q; i++) {
    int t;
    cin >> t;
    out += to_string(dist[t]);
    out += '\n';
  }
  cout << out;
}
