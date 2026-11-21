// Reference for lp_sp01_delivery_times: Dijkstra with a priority_queue and lazy
// deletion, O((N + M) log M). Distances reach (N - 1) * 10^6, so long long.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m, s;
  cin >> n >> m >> s;
  vector<vector<pair<int, int>>> adj(n + 1);
  for (int i = 0; i < m; i++) {
    int u, v, w;
    cin >> u >> v >> w;
    adj[u].push_back({v, w});
    adj[v].push_back({u, w});
  }
  const long long INF = LLONG_MAX;
  vector<long long> dist(n + 1, INF);
  priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<>> pq;
  dist[s] = 0;
  pq.push({0, s});
  while (!pq.empty()) {
    auto [d, u] = pq.top();
    pq.pop();
    if (d > dist[u]) continue;
    for (auto [v, w] : adj[u]) {
      if (dist[u] + w < dist[v]) {
        dist[v] = dist[u] + w;
        pq.push({dist[v], v});
      }
    }
  }
  for (int v = 1; v <= n; v++) cout << (dist[v] == INF ? -1 : dist[v]) << (v == n ? '\n' : ' ');
}
