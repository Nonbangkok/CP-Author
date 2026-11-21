// Naive: for each query, count walks step by step over the edge list,
// cnt'[v] = sum of cnt[u] over corridors u -> v. O(Q * L * (N + M)) --
// fine for L <= 500, hopeless for L ~ 10^18.
#include <bits/stdc++.h>
using namespace std;

const long long MOD = 1000000007LL;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m, q;
  cin >> n >> m >> q;
  vector<int> from(m), to(m);
  for (int e = 0; e < m; e++) {
    cin >> from[e] >> to[e];
    from[e]--;
    to[e]--;
  }
  while (q--) {
    int s, t;
    long long len;
    cin >> s >> t >> len;
    vector<long long> cnt(n, 0), nxt(n);
    cnt[s - 1] = 1;
    for (long long step = 0; step < len; step++) {
      fill(nxt.begin(), nxt.end(), 0);
      for (int e = 0; e < m; e++) nxt[to[e]] = (nxt[to[e]] + cnt[from[e]]) % MOD;
      swap(cnt, nxt);
    }
    cout << cnt[t - 1] << '\n';
  }
}
