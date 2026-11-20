// Reference for lp_lca01_family_tree: binary lifting. up[k][v] = the 2^k-th
// ancestor of v (the root is its own parent). Lift the deeper person to the
// same depth, then lift both while their 2^k-th ancestors differ.
// O((N + Q) log N); depths from a BFS order (no recursion).
#include <bits/stdc++.h>
using namespace std;

const int LOG = 17;  // 2^17 > 10^5
int up[LOG][100001];
int depth_[100001];

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

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, q;
  cin >> n >> q;
  vector<vector<int>> children(n + 1);
  up[0][1] = 1;
  for (int i = 2; i <= n; i++) {
    cin >> up[0][i];
    children[up[0][i]].push_back(i);
  }
  vector<int> order = {1};
  depth_[1] = 0;
  for (int i = 0; i < (int)order.size(); i++)
    for (int c : children[order[i]]) {
      depth_[c] = depth_[order[i]] + 1;
      order.push_back(c);
    }
  for (int k = 1; k < LOG; k++)
    for (int v = 1; v <= n; v++) up[k][v] = up[k - 1][up[k - 1][v]];
  while (q--) {
    int u, v;
    cin >> u >> v;
    cout << lca(u, v) << '\n';
  }
}
