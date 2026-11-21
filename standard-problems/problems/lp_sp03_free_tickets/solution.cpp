// Reference for lp_sp03_free_tickets: Dijkstra on the state graph (city, tickets
// used). State id = city * (K + 1) + used; N (K + 1) states and 4 M (K + 1) arcs,
// O(M K log(M K)). Riding pays w and keeps used; a ticket costs 0 and adds one.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m, k;
  cin >> n >> m >> k;
  vector<vector<pair<int, int>>> adj(n + 1);
  for (int i = 0; i < m; i++) {
    int u, v, w;
    cin >> u >> v >> w;
    adj[u].push_back({v, w});
    adj[v].push_back({u, w});
  }
  int layers = k + 1;
  const long long INF = LLONG_MAX;
  vector<long long> dist((n + 1) * layers, INF);
  priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<>> pq;
  dist[1 * layers + 0] = 0;
  pq.push({0, 1 * layers + 0});
  while (!pq.empty()) {
    auto [d, s] = pq.top();
    pq.pop();
    if (d > dist[s]) continue;
    int u = s / layers, used = s % layers;
    for (auto [v, w] : adj[u]) {
      int t = v * layers + used;
      if (d + w < dist[t]) {  // pay for this ride
        dist[t] = d + w;
        pq.push({dist[t], t});
      }
      if (used < k && d < dist[t + 1]) {  // use a free ticket
        dist[t + 1] = d;
        pq.push({d, t + 1});
      }
    }
  }
  long long best = INF;
  for (int used = 0; used <= k; used++) best = min(best, dist[n * layers + used]);
  cout << (best == INF ? -1 : best) << '\n';
}
