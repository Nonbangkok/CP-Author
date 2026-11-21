// Reference for lp_mst01_fiber_network: Kruskal with a DSU (union by size +
// path compression). Sort edges by cost, take an edge whenever its ends are in
// different components; the network is connected iff N - 1 edges were taken.
// O(M log M).
#include <bits/stdc++.h>
using namespace std;

vector<int> parent, sz;

int find(int x) {
  while (parent[x] != x) {
    parent[x] = parent[parent[x]];  // path halving
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
  vector<array<int, 3>> edges(m);  // {w, u, v}
  for (auto &e : edges) cin >> e[1] >> e[2] >> e[0];
  sort(edges.begin(), edges.end());
  parent.resize(n + 1);
  sz.assign(n + 1, 1);
  iota(parent.begin(), parent.end(), 0);
  long long total = 0;
  int taken = 0;
  for (auto [w, u, v] : edges) {
    if (unite(u, v)) {
      total += w;
      taken++;
    }
  }
  cout << (taken == n - 1 ? total : -1) << '\n';
}
