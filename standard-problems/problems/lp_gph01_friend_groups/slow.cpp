// Naive: every person starts with their own group label; for each friendship
// whose two ends carry different labels, relabel the whole second group by
// scanning all N people. Correct, but O(N * M): times out on the last subtask.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m;
  cin >> n >> m;
  vector<int> label(n + 1);
  for (int i = 1; i <= n; i++) label[i] = i;
  for (int i = 0; i < m; i++) {
    int u, v;
    cin >> u >> v;
    int from = label[v], to = label[u];
    if (from == to) continue;
    for (int x = 1; x <= n; x++)
      if (label[x] == from) label[x] = to;
  }
  vector<int> count(n + 1, 0);
  int groups = 0, largest = 0;
  for (int x = 1; x <= n; x++) {
    if (count[label[x]]++ == 0) groups++;
    largest = max(largest, count[label[x]]);
  }
  cout << groups << ' ' << largest << '\n';
}
