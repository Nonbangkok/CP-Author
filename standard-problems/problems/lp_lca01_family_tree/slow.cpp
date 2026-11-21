// Naive: climb one parent at a time. Bring the deeper person up to the same
// depth, then move both up together until they meet. O(depth) per query:
// fine for N, Q <= 5,000, times out on a path of 10^5 people.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, q;
  cin >> n >> q;
  vector<int> par(n + 1, 0), depth(n + 1, 0);
  vector<vector<int>> children(n + 1);
  for (int i = 2; i <= n; i++) {
    cin >> par[i];
    children[par[i]].push_back(i);
  }
  vector<int> order = {1};
  for (int i = 0; i < (int)order.size(); i++)
    for (int c : children[order[i]]) {
      depth[c] = depth[order[i]] + 1;
      order.push_back(c);
    }
  while (q--) {
    int u, v;
    cin >> u >> v;
    while (depth[u] > depth[v]) u = par[u];
    while (depth[v] > depth[u]) v = par[v];
    while (u != v) {
      u = par[u];
      v = par[v];
    }
    cout << u << '\n';
  }
}
