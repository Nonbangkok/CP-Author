// Reference for lp_tr02_longest_trail: the diameter with two passes. The hut
// farthest from any hut is one end of a longest trail; the hut farthest from
// that end is the other. Iterative DFS (a path of 10^5 huts would overflow the
// stack with recursion); lengths are positive, so this is valid. O(N).
#include <bits/stdc++.h>
using namespace std;

int n;
vector<vector<pair<int, int>>> adj;

// distance from s to every hut; returns the farthest hut
int farthest(int s, vector<long long> &dist) {
  dist.assign(n + 1, -1);
  dist[s] = 0;
  vector<int> st = {s};
  int best = s;
  while (!st.empty()) {
    int u = st.back();
    st.pop_back();
    if (dist[u] > dist[best]) best = u;
    for (auto [v, w] : adj[u])
      if (dist[v] < 0) {
        dist[v] = dist[u] + w;
        st.push_back(v);
      }
  }
  return best;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  cin >> n;
  adj.resize(n + 1);
  for (int i = 0; i < n - 1; i++) {
    int u, v, w;
    cin >> u >> v >> w;
    adj[u].push_back({v, w});
    adj[v].push_back({u, w});
  }
  vector<long long> dist;
  int a = farthest(1, dist);
  int b = farthest(a, dist);
  cout << dist[b] << '\n';
}
