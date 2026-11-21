// Naive Kruskal: sort the edges, and before taking one, walk the forest built so
// far (DFS from u) to see whether v is already reachable. Correct, but every
// check can visit the whole forest: O(M * N), times out on the last subtask.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m;
  cin >> n >> m;
  vector<array<int, 3>> edges(m);  // {w, u, v}
  for (auto &e : edges) cin >> e[1] >> e[2] >> e[0];
  sort(edges.begin(), edges.end());
  vector<vector<int>> forest(n + 1);
  long long total = 0;
  int taken = 0;
  for (auto [w, u, v] : edges) {
    if (taken == n - 1) break;
    vector<char> seen(n + 1, 0);
    vector<int> stack = {u};
    seen[u] = 1;
    bool reached = false;
    while (!stack.empty() && !reached) {
      int x = stack.back();
      stack.pop_back();
      for (int y : forest[x]) {
        if (!seen[y]) {
          seen[y] = 1;
          if (y == v) reached = true;
          stack.push_back(y);
        }
      }
    }
    if (!reached) {
      forest[u].push_back(v);
      forest[v].push_back(u);
      total += w;
      taken++;
    }
  }
  cout << (taken == n - 1 ? total : -1) << '\n';
}
