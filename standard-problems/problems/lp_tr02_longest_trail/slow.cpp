// Naive: search from every hut and keep the largest distance seen. O(N^2):
// fine for N <= 2,000, times out on N = 5*10^4.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<vector<pair<int, int>>> adj(n + 1);
  for (int i = 0; i < n - 1; i++) {
    int u, v, w;
    cin >> u >> v >> w;
    adj[u].push_back({v, w});
    adj[v].push_back({u, w});
  }
  long long best = 0;
  vector<long long> dist(n + 1);
  vector<int> st;
  for (int s = 1; s <= n; s++) {
    fill(dist.begin(), dist.end(), -1);
    dist[s] = 0;
    st.assign(1, s);
    while (!st.empty()) {
      int u = st.back();
      st.pop_back();
      best = max(best, dist[u]);
      for (auto [v, w] : adj[u])
        if (dist[v] < 0) {
          dist[v] = dist[u] + w;
          st.push_back(v);
        }
    }
  }
  cout << best << '\n';
}
