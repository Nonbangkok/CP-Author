// Naive: the same distance formula, but the LCA climbs one edge at a time.
// O(depth) per query: fine for N, Q <= 5,000, times out on a path of 5*10^4.
#include <bits/stdc++.h>
using namespace std;

vector<int> par, depth_;
vector<long long> dist_;

int lca(int u, int v) {
  while (depth_[u] > depth_[v]) u = par[u];
  while (depth_[v] > depth_[u]) v = par[v];
  while (u != v) {
    u = par[u];
    v = par[v];
  }
  return u;
}

long long distance(int u, int v) { return dist_[u] + dist_[v] - 2 * dist_[lca(u, v)]; }

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, q;
  cin >> n >> q;
  vector<vector<pair<int, int>>> adj(n + 1);
  for (int i = 0; i < n - 1; i++) {
    int u, v, w;
    cin >> u >> v >> w;
    adj[u].push_back({v, w});
    adj[v].push_back({u, w});
  }
  par.assign(n + 1, 0);
  depth_.assign(n + 1, 0);
  dist_.assign(n + 1, 0);
  vector<int> order = {1};
  vector<bool> seen(n + 1, false);
  seen[1] = true;
  for (int i = 0; i < (int)order.size(); i++) {
    int u = order[i];
    for (auto [v, w] : adj[u])
      if (!seen[v]) {
        seen[v] = true;
        par[v] = u;
        depth_[v] = depth_[u] + 1;
        dist_[v] = dist_[u] + w;
        order.push_back(v);
      }
  }
  while (q--) {
    int a, b, c;
    cin >> a >> b >> c;
    cout << distance(a, c) + distance(c, b) - distance(a, b) << '\n';
  }
}
