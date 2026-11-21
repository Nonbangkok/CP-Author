// Reference for lp_tr03_office_party: tree DP with two states per employee.
// take[v] = f[v] + sum skip[c]; skip[v] = sum max(take[c], skip[c]) over the
// direct reports c. A BFS order from the CEO walked backwards handles every
// report before its boss (no recursion: the chain of command can be 10^5 deep).
// O(N).
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<long long> f(n + 1);
  for (int i = 1; i <= n; i++) cin >> f[i];
  vector<int> boss(n + 1, 0);
  vector<vector<int>> reports(n + 1);
  for (int i = 2; i <= n; i++) {
    cin >> boss[i];
    reports[boss[i]].push_back(i);
  }
  vector<int> order = {1};
  for (int i = 0; i < (int)order.size(); i++)
    for (int c : reports[order[i]]) order.push_back(c);

  vector<long long> take(n + 1, 0), skip(n + 1, 0);
  for (int i = n - 1; i >= 0; i--) {
    int v = order[i];
    take[v] += f[v];
    if (v != 1) {
      take[boss[v]] += skip[v];
      skip[boss[v]] += max(take[v], skip[v]);
    }
  }
  cout << max(take[1], skip[1]) << '\n';
}
