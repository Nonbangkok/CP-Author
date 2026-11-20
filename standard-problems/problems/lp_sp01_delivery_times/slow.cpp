// Naive Dijkstra without a heap: every round scans all N vertices for the
// closest unfinished one, O(N^2 + M). Correct, and must time out on the last
// subtask (N = 5 * 10^4).
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
  vector<char> done(n + 1, 0);
  dist[s] = 0;
  for (int round = 0; round < n; round++) {
    int u = -1;
    for (int v = 1; v <= n; v++)
      if (!done[v] && (u == -1 || dist[v] < dist[u])) u = v;
    if (dist[u] == INF) break;
    done[u] = 1;
    for (auto [v, w] : adj[u])
      if (dist[u] + w < dist[v]) dist[v] = dist[u] + w;
  }
  for (int v = 1; v <= n; v++) cout << (dist[v] == INF ? -1 : dist[v]) << (v == n ? '\n' : ' ');
}
