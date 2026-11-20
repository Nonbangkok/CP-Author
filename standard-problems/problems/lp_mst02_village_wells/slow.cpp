// Naive: the same virtual-vertex graph, but Prim without a heap -- every step
// scans all vertices for the cheapest one not yet in the tree. O(N^2 + M),
// fine for a few thousand villages, times out on the last subtask.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m;
  cin >> n >> m;
  vector<vector<pair<int, int>>> adj(n + 1);
  for (int i = 1; i <= n; i++) {
    int c;
    cin >> c;
    adj[0].push_back({i, c});
    adj[i].push_back({0, c});
  }
  for (int j = 0; j < m; j++) {
    int u, v, w;
    cin >> u >> v >> w;
    adj[u].push_back({v, w});
    adj[v].push_back({u, w});
  }
  const long long INF = LLONG_MAX;
  vector<long long> key(n + 1, INF);
  vector<char> inTree(n + 1, 0);
  key[0] = 0;
  long long total = 0;
  for (int step = 0; step <= n; step++) {
    int best = -1;
    for (int v = 0; v <= n; v++)
      if (!inTree[v] && (best == -1 || key[v] < key[best])) best = v;
    inTree[best] = 1;
    total += key[best];
    for (auto [v, w] : adj[best])
      if (!inTree[v] && w < key[v]) key[v] = w;
  }
  cout << total << '\n';
}
