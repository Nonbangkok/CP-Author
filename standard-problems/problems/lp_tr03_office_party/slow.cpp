// Naive: the right recurrence but no memo. best(v) = max(f[v] + best of every
// grandchild, best of every child) recomputes the same subtrees again and
// again: on a chain of depth D it makes about Fib(D) calls. Fine for N <= 30,
// times out on a 100-deep chain of command.
#include <bits/stdc++.h>
using namespace std;

vector<long long> f;
vector<vector<int>> reports;

long long best(int v) {
  long long with = f[v], without = 0;
  for (int c : reports[v]) {
    without += best(c);
    for (int g : reports[c]) with += best(g);
  }
  return max(with, without);
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  f.resize(n + 1);
  reports.resize(n + 1);
  for (int i = 1; i <= n; i++) cin >> f[i];
  for (int i = 2; i <= n; i++) {
    int p;
    cin >> p;
    reports[p].push_back(i);
  }
  cout << best(1) << '\n';
}
