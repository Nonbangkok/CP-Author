// Reference for lp_bit02_party_planning: enumerate every mask of the N <= 20
// friends. cost[], fun[] and ok[] of a mask come from the mask without its
// lowest set bit, so the whole table is O(2^N).
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m;
  long long budget;
  cin >> n >> m >> budget;
  vector<long long> c(n), v(n);
  for (int i = 0; i < n; i++) cin >> c[i] >> v[i];
  vector<int> conflict(n, 0);
  for (int j = 0; j < m; j++) {
    int x, y;
    cin >> x >> y;
    x--, y--;
    conflict[x] |= 1 << y;
    conflict[y] |= 1 << x;
  }
  int total = 1 << n;
  vector<long long> cost(total, 0), fun(total, 0);
  vector<char> ok(total, 1);
  long long best = 0;
  for (int mask = 1; mask < total; mask++) {
    int i = __builtin_ctz(mask);
    int rest = mask & (mask - 1);
    cost[mask] = cost[rest] + c[i];
    fun[mask] = fun[rest] + v[i];
    ok[mask] = ok[rest] && (conflict[i] & rest) == 0;
    if (ok[mask] && cost[mask] <= budget) best = max(best, fun[mask]);
  }
  cout << best << '\n';
}
