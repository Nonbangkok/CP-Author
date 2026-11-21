// Naive: the same state graph (city, tickets used), but Dijkstra without a heap
// scans all N * (K + 1) states every round, O((N K)^2). Correct, and must time
// out on the last subtask.
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
  int layers = k + 1, states = (n + 1) * layers;
  const long long INF = LLONG_MAX;
  vector<long long> dist(states, INF);
  vector<char> done(states, 0);
  dist[1 * layers + 0] = 0;
  while (true) {
    int best = -1;
    for (int s = layers; s < states; s++)
      if (!done[s] && dist[s] != INF && (best == -1 || dist[s] < dist[best])) best = s;
    if (best == -1) break;
    done[best] = 1;
    int u = best / layers, used = best % layers;
    for (auto [v, w] : adj[u]) {
      int pay = v * layers + used;
      if (dist[best] + w < dist[pay]) dist[pay] = dist[best] + w;
      if (used < k && dist[best] < dist[pay + 1]) dist[pay + 1] = dist[best];
    }
  }
  long long answer = INF;
  for (int used = 0; used <= k; used++) answer = min(answer, dist[n * layers + used]);
  cout << (answer == INF ? -1 : answer) << '\n';
}
