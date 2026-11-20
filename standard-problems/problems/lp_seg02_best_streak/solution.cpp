// Reference for lp_seg02_best_streak: segment tree whose node is a struct
// (sum, best prefix, best suffix, best subarray) of its segment; point
// assignment and range query, O(log N) each. The query never merges with an
// "empty" node: it only recurses into the halves that overlap [l, r].
#include <bits/stdc++.h>
using namespace std;

struct Node {
  long long sum, pref, suf, best;
};

Node make_leaf(long long x) { return {x, x, x, x}; }

Node merge(const Node &L, const Node &R) {
  Node res;
  res.sum = L.sum + R.sum;
  res.pref = max(L.pref, L.sum + R.pref);
  res.suf = max(R.suf, R.sum + L.suf);
  res.best = max({L.best, R.best, L.suf + R.pref});
  return res;
}

int n;
vector<long long> a;
vector<Node> t;

void build(int v, int tl, int tr) {
  if (tl == tr) { t[v] = make_leaf(a[tl]); return; }
  int tm = (tl + tr) / 2;
  build(2 * v, tl, tm);
  build(2 * v + 1, tm + 1, tr);
  t[v] = merge(t[2 * v], t[2 * v + 1]);
}

void update(int v, int tl, int tr, int pos, long long x) {
  if (tl == tr) { t[v] = make_leaf(x); return; }
  int tm = (tl + tr) / 2;
  if (pos <= tm) update(2 * v, tl, tm, pos, x);
  else update(2 * v + 1, tm + 1, tr, pos, x);
  t[v] = merge(t[2 * v], t[2 * v + 1]);
}

// requires tl <= l <= r <= tr
Node query(int v, int tl, int tr, int l, int r) {
  if (l == tl && r == tr) return t[v];
  int tm = (tl + tr) / 2;
  if (r <= tm) return query(2 * v, tl, tm, l, r);
  if (l > tm) return query(2 * v + 1, tm + 1, tr, l, r);
  return merge(query(2 * v, tl, tm, l, tm), query(2 * v + 1, tm + 1, tr, tm + 1, r));
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int q;
  cin >> n >> q;
  a.assign(n + 1, 0);
  t.assign(4 * n, Node{0, 0, 0, 0});
  for (int i = 1; i <= n; i++) cin >> a[i];
  build(1, 1, n);
  string out;
  while (q--) {
    int type;
    long long x, y;
    cin >> type >> x >> y;
    if (type == 1) update(1, 1, n, (int)x, y);
    else { out += to_string(query(1, 1, n, (int)x, (int)y).best); out += '\n'; }
  }
  cout << out;
}
