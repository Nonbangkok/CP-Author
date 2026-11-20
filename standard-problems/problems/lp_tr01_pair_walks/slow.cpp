// Naive: BFS from every house and add up all distances (each pair is counted
// twice). O(N^2): fine for N <= 4,000, times out on N = 10^5.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<vector<int>> adj(n + 1);
  for (int i = 0; i < n - 1; i++) {
    int u, v;
    cin >> u >> v;
    adj[u].push_back(v);
    adj[v].push_back(u);
  }
  long long total = 0;
  vector<int> dist(n + 1), q(n);
  for (int s = 1; s <= n; s++) {
    fill(dist.begin(), dist.end(), -1);
    int head = 0, tail = 0;
    q[tail++] = s;
    dist[s] = 0;
    while (head < tail) {
      int u = q[head++];
      total += dist[u];
      for (int v : adj[u])
        if (dist[v] < 0) {
          dist[v] = dist[u] + 1;
          q[tail++] = v;
        }
    }
  }
  cout << total / 2 << '\n';
}
