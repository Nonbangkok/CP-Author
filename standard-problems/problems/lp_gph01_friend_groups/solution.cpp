// Reference for lp_gph01_friend_groups: adjacency list + iterative DFS from
// every unvisited vertex; each DFS is one component, count its vertices.
// O(N + M).
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m;
  cin >> n >> m;
  vector<vector<int>> adj(n + 1);
  for (int i = 0; i < m; i++) {
    int u, v;
    cin >> u >> v;
    adj[u].push_back(v);
    adj[v].push_back(u);
  }
  vector<char> seen(n + 1, 0);
  int groups = 0, largest = 0;
  vector<int> st;
  for (int s = 1; s <= n; s++) {
    if (seen[s]) continue;
    groups++;
    int size = 0;
    seen[s] = 1;
    st.push_back(s);
    while (!st.empty()) {
      int u = st.back();
      st.pop_back();
      size++;
      for (int v : adj[u]) {
        if (!seen[v]) {
          seen[v] = 1;
          st.push_back(v);
        }
      }
    }
    largest = max(largest, size);
  }
  cout << groups << ' ' << largest << '\n';
}
