// Naive: run a fresh BFS from city 1 for every query, stopping early when the
// target is reached. Correct, but O(Q * (N + M)): times out on the last subtask.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m, q;
  cin >> n >> m >> q;
  vector<vector<int>> adj(n + 1);
  for (int i = 0; i < m; i++) {
    int a, b;
    cin >> a >> b;
    adj[a].push_back(b);
  }
  vector<int> dist(n + 1);
  for (int i = 0; i < q; i++) {
    int t;
    cin >> t;
    fill(dist.begin(), dist.end(), -1);
    queue<int> bfs;
    dist[1] = 0;
    bfs.push(1);
    while (!bfs.empty() && dist[t] == -1) {
      int u = bfs.front();
      bfs.pop();
      for (int v : adj[u]) {
        if (dist[v] == -1) {
          dist[v] = dist[u] + 1;
          bfs.push(v);
        }
      }
    }
    cout << dist[t] << '\n';
  }
}
