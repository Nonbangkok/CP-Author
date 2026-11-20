// Reference for lp_tr01_pair_walks: every road u-v (v the child when rooted at
// 1) is walked by exactly sz[v] * (N - sz[v]) pairs, so the answer is the sum
// of that over all roads. Subtree sizes with an iterative DFS (a path of
// 2*10^5 vertices would overflow the stack with recursion). O(N).
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
  vector<int> parent(n + 1, 0), order;
  order.reserve(n);
  vector<int> st = {1};
  parent[1] = -1;
  while (!st.empty()) {
    int u = st.back();
    st.pop_back();
    order.push_back(u);
    for (int v : adj[u])
      if (v != parent[u]) {
        parent[v] = u;
        st.push_back(v);
      }
  }
  vector<long long> sz(n + 1, 1);
  long long answer = 0;
  for (int i = n - 1; i >= 1; i--) {  // children before parents
    int v = order[i];
    sz[parent[v]] += sz[v];
    answer += sz[v] * (n - sz[v]);
  }
  cout << answer << '\n';
}
