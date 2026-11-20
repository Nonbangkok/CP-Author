// Naive: after each new rivalry, rebuild the graph and run the BFS
// two-colouring from scratch. Correct, but O(M * (N + M)) when the answer is
// late (or -1): times out on the last subtask.
#include <bits/stdc++.h>
using namespace std;

int n, m;
vector<int> eu, ev;

bool splittable(int k) {
  vector<vector<int>> adj(n + 1);
  for (int i = 0; i < k; i++) {
    adj[eu[i]].push_back(ev[i]);
    adj[ev[i]].push_back(eu[i]);
  }
  vector<int> color(n + 1, -1);
  for (int s = 1; s <= n; s++) {
    if (color[s] != -1) continue;
    color[s] = 0;
    queue<int> q;
    q.push(s);
    while (!q.empty()) {
      int u = q.front();
      q.pop();
      for (int v : adj[u]) {
        if (color[v] == -1) {
          color[v] = 1 - color[u];
          q.push(v);
        } else if (color[v] == color[u]) {
          return false;
        }
      }
    }
  }
  return true;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  cin >> n >> m;
  eu.resize(m);
  ev.resize(m);
  for (int i = 0; i < m; i++) cin >> eu[i] >> ev[i];
  for (int k = 1; k <= m; k++) {
    if (!splittable(k)) {
      cout << k << '\n';
      return 0;
    }
  }
  cout << -1 << '\n';
}
