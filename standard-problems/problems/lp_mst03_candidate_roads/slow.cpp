// Naive: for every road, BFS from u using only strictly cheaper roads and see
// whether v is reached (cycle property). O(M * (N + M)): fine for a few
// thousand roads, times out on the last subtask.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m;
  cin >> n >> m;
  vector<int> u(m), v(m), w(m);
  vector<vector<pair<int, int>>> adj(n + 1);  // (neighbour, weight)
  for (int i = 0; i < m; i++) {
    cin >> u[i] >> v[i] >> w[i];
    adj[u[i]].push_back({v[i], w[i]});
    adj[v[i]].push_back({u[i], w[i]});
  }
  for (int i = 0; i < m; i++) {
    vector<char> seen(n + 1, 0);
    queue<int> q;
    q.push(u[i]);
    seen[u[i]] = 1;
    while (!q.empty() && !seen[v[i]]) {
      int x = q.front();
      q.pop();
      for (auto [y, c] : adj[x]) {
        if (c < w[i] && !seen[y]) {
          seen[y] = 1;
          q.push(y);
        }
      }
    }
    cout << (seen[v[i]] ? "NO" : "YES") << '\n';
  }
}
