// Reference for lp_mst03_candidate_roads. An edge (u, v, w) is in some MST iff
// u and v are NOT connected by edges of weight < w (cycle property). Kruskal
// in groups of equal weight: first answer every edge of the group with
// find(u) != find(v) using only lighter edges, then unite the whole group.
// O(M log M).
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

void unite(int a, int b) {
  a = find(a);
  b = find(b);
  if (a == b) return;
  if (sz[a] < sz[b]) swap(a, b);
  parent[b] = a;
  sz[a] += sz[b];
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m;
  cin >> n >> m;
  vector<int> u(m), v(m), w(m);
  for (int i = 0; i < m; i++) cin >> u[i] >> v[i] >> w[i];
  vector<int> order(m);
  iota(order.begin(), order.end(), 0);
  sort(order.begin(), order.end(), [&](int a, int b) { return w[a] < w[b]; });
  parent.resize(n + 1);
  sz.assign(n + 1, 1);
  iota(parent.begin(), parent.end(), 0);
  vector<char> yes(m, 0);
  for (int i = 0; i < m;) {
    int j = i;
    while (j < m && w[order[j]] == w[order[i]]) j++;
    for (int k = i; k < j; k++) {
      int e = order[k];
      yes[e] = find(u[e]) != find(v[e]);
    }
    for (int k = i; k < j; k++) unite(u[order[k]], v[order[k]]);
    i = j;
  }
  string out;
  out.reserve(4 * m);
  for (int i = 0; i < m; i++) out += yes[i] ? "YES\n" : "NO\n";
  cout << out;
}
