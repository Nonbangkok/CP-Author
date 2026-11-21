// Reference for lp_mst02_village_wells: add a virtual vertex 0 ("the ground
// water") with an edge 0 - i of cost c_i for every village. A valid plan is a
// spanning tree of vertices 0..N, so the answer is the MST weight of that
// graph (Kruskal + DSU). O((N + M) log(N + M)).
#include <bits/stdc++.h>
using namespace std;

vector<int> parent, sz;

int find(int x) {
  while (parent[x] != x) {
    parent[x] = parent[parent[x]];
    x = parent[x];
  }
  return x;
}

bool unite(int a, int b) {
  a = find(a);
  b = find(b);
  if (a == b) return false;
  if (sz[a] < sz[b]) swap(a, b);
  parent[b] = a;
  sz[a] += sz[b];
  return true;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m;
  cin >> n >> m;
  vector<array<int, 3>> edges;  // {w, u, v}
  edges.reserve(n + m);
  for (int i = 1; i <= n; i++) {
    int c;
    cin >> c;
    edges.push_back({c, 0, i});
  }
  for (int j = 0; j < m; j++) {
    int u, v, w;
    cin >> u >> v >> w;
    edges.push_back({w, u, v});
  }
  sort(edges.begin(), edges.end());
  parent.resize(n + 1);
  sz.assign(n + 1, 1);
  iota(parent.begin(), parent.end(), 0);
  long long total = 0;
  for (auto [w, u, v] : edges)
    if (unite(u, v)) total += w;
  cout << total << '\n';
}
