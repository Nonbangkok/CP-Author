// Reference for lp_fw02_bonus_points: range add + point query with a Fenwick
// tree over the difference array d (d[i] = a[i] - a[i-1]). "Add x to [l, r]"
// is d[l] += x, d[r+1] -= x; the score of i is a[i] (kept apart) plus the
// prefix sum of the added differences. O((N + Q) log N). A score can move by up
// to 5 * 10^4 * 10^6 = 5 * 10^10, so long long.
#include <bits/stdc++.h>
using namespace std;

int n;
vector<long long> bit;

void add(int i, long long delta) {
  for (; i <= n; i += i & -i) bit[i] += delta;
}

long long prefix(int i) {
  long long s = 0;
  for (; i > 0; i -= i & -i) s += bit[i];
  return s;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int q;
  cin >> n >> q;
  vector<long long> a(n + 1);
  for (int i = 1; i <= n; i++) cin >> a[i];
  bit.assign(n + 1, 0);
  while (q--) {
    int type;
    cin >> type;
    if (type == 1) {
      int l, r;
      long long x;
      cin >> l >> r >> x;
      add(l, x);
      if (r + 1 <= n) add(r + 1, -x);
    } else {
      int i;
      cin >> i;
      cout << a[i] + prefix(i) << '\n';
    }
  }
}
