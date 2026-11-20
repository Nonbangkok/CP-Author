// Reference for lp_lazy01_coin_towers: lazy segment tree, node = sum of its
// segment, tag = coins still owed to every pile below it. Applying "+v" to a
// node of length len adds v * len to its sum. O(log N) per event.
#include <bits/stdc++.h>
using namespace std;

int n;
vector<long long> a, sum, add;

void apply(int v, int tl, int tr, long long x) {
  sum[v] += x * (tr - tl + 1);
  add[v] += x;
}

void push(int v, int tl, int tr) {
  if (add[v] != 0) {
    int tm = (tl + tr) / 2;
    apply(2 * v, tl, tm, add[v]);
    apply(2 * v + 1, tm + 1, tr, add[v]);
    add[v] = 0;
  }
}

void build(int v, int tl, int tr) {
  if (tl == tr) { sum[v] = a[tl]; return; }
  int tm = (tl + tr) / 2;
  build(2 * v, tl, tm);
  build(2 * v + 1, tm + 1, tr);
  sum[v] = sum[2 * v] + sum[2 * v + 1];
}

void update(int v, int tl, int tr, int l, int r, long long x) {
  if (r < tl || tr < l) return;
  if (l <= tl && tr <= r) { apply(v, tl, tr, x); return; }
  push(v, tl, tr);
  int tm = (tl + tr) / 2;
  update(2 * v, tl, tm, l, r, x);
  update(2 * v + 1, tm + 1, tr, l, r, x);
  sum[v] = sum[2 * v] + sum[2 * v + 1];
}

long long query(int v, int tl, int tr, int l, int r) {
  if (r < tl || tr < l) return 0;
  if (l <= tl && tr <= r) return sum[v];
  push(v, tl, tr);
  int tm = (tl + tr) / 2;
  return query(2 * v, tl, tm, l, r) + query(2 * v + 1, tm + 1, tr, l, r);
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int q;
  cin >> n >> q;
  a.assign(n + 1, 0);
  sum.assign(4 * n, 0);
  add.assign(4 * n, 0);
  for (int i = 1; i <= n; i++) cin >> a[i];
  build(1, 1, n);
  string out;
  while (q--) {
    int type, l, r;
    cin >> type >> l >> r;
    if (type == 1) {
      long long v;
      cin >> v;
      update(1, 1, n, l, r, v);
    } else {
      out += to_string(query(1, 1, n, l, r));
      out += '\n';
    }
  }
  cout << out;
}
