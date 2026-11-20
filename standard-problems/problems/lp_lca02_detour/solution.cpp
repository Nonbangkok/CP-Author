// Reference for lp_lca02_detour: root the tree at 1, keep dist[v] = length
// from the root, and dist(x, y) = dist[x] + dist[y] - 2 * dist[lca(x, y)] with
// binary lifting. The answer is dist(a, c) + dist(c, b) - dist(a, b), which is
// 0 exactly when c lies on the path a-b. O((N + Q) log N), no recursion.
#include <bits/stdc++.h>
using namespace std;

const int LOG = 16;  // 2^16 > 5*10^4
const int MAXN = 50001;
int up[LOG][MAXN];
int depth_[MAXN];
long long dist_[MAXN];

int lca(int u, int v) {
  if (depth_[u] < depth_[v]) swap(u, v);
  int diff = depth_[u] - depth_[v];
  for (int k = 0; k < LOG; k++)
    if (diff >> k & 1) u = up[k][u];
  if (u == v) return u;
  for (int k = LOG - 1; k >= 0; k--)
    if (up[k][u] != up[k][v]) {
      u = up[k][u];
      v = up[k][v];
    }
  return up[0][u];
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
  vector<int> order = {1};
  vector<bool> seen(n + 1, false);
  seen[1] = true;
  up[0][1] = 1;
  for (int i = 0; i < (int)order.size(); i++) {
    int u = order[i];
    for (auto [v, w] : adj[u])
      if (!seen[v]) {
        seen[v] = true;
        up[0][v] = u;
        depth_[v] = depth_[u] + 1;
        dist_[v] = dist_[u] + w;
        order.push_back(v);
      }
  }
  for (int k = 1; k < LOG; k++)
    for (int v = 1; v <= n; v++) up[k][v] = up[k - 1][up[k - 1][v]];
  while (q--) {
    int a, b, c;
    cin >> a >> b >> c;
    cout << distance(a, c) + distance(c, b) - distance(a, b) << '\n';
  }
}
