// Naive: a fresh Bellman-Ford (with early exit) for every query, O(Q * N * M).
// Correct with negative weights, and must time out on the last subtask.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m, q;
  cin >> n >> m >> q;
  vector<array<long long, 3>> edges(m);
  for (auto &e : edges) cin >> e[0] >> e[1] >> e[2];
  const long long INF = LLONG_MAX;
  vector<long long> dist(n + 1);
  while (q--) {
    int a, b;
    cin >> a >> b;
    fill(dist.begin(), dist.end(), INF);
    dist[a] = 0;
    for (int round = 1; round < n; round++) {
      bool changed = false;
      for (auto &e : edges)
        if (dist[e[0]] != INF && dist[e[0]] + e[2] < dist[e[1]]) {
          dist[e[1]] = dist[e[0]] + e[2];
          changed = true;
        }
      if (!changed) break;
    }
    if (dist[b] == INF) cout << "NO\n";
    else cout << dist[b] << '\n';
  }
}
