// Reference for lp_gph03_rival_teams: "rivalries 1..k can be split into two
// teams" is true ... true false ... false in k (adding edges never helps), so
// binary search on k with a BFS two-colouring as the check.
// O((N + M) log M).
#include <bits/stdc++.h>
using namespace std;

int n, m;
vector<int> eu, ev;

// Can the first k rivalries be split into two teams? BFS 2-colouring.
bool splittable(int k) {
  vector<vector<int>> adj(n + 1);
  for (int i = 0; i < k; i++) {
    adj[eu[i]].push_back(ev[i]);
    adj[ev[i]].push_back(eu[i]);
  }
  vector<int> color(n + 1, -1);
  vector<int> q;
  for (int s = 1; s <= n; s++) {
    if (color[s] != -1) continue;
    color[s] = 0;
    q.assign(1, s);
    for (size_t head = 0; head < q.size(); head++) {
      int u = q[head];
      for (int v : adj[u]) {
        if (color[v] == -1) {
          color[v] = 1 - color[u];
          q.push_back(v);
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
  if (splittable(m)) {
    cout << -1 << '\n';
    return 0;
  }
  int lo = 0, hi = m;  // splittable(lo) is true, splittable(hi) is false
  while (hi - lo > 1) {
    int mid = lo + (hi - lo) / 2;
    if (splittable(mid)) lo = mid;
    else hi = mid;
  }
  cout << hi << '\n';
}
