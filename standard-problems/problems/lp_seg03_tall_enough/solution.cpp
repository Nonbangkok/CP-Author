// Reference for lp_seg03_tall_enough: segment tree of maximums. A query walks
// down the tree: a node whose maximum is below x (or outside [l, r]) is skipped
// whole; otherwise the left child is tried before the right one. Only the
// nodes along one failing path and one successful path are opened, so a query
// costs O(log N); a point assignment also costs O(log N).
#include <bits/stdc++.h>
using namespace std;

int n;
vector<int> h, t;

void build(int v, int tl, int tr) {
  if (tl == tr) { t[v] = h[tl]; return; }
  int tm = (tl + tr) / 2;
  build(2 * v, tl, tm);
  build(2 * v + 1, tm + 1, tr);
  t[v] = max(t[2 * v], t[2 * v + 1]);
}

void update(int v, int tl, int tr, int pos, int y) {
  if (tl == tr) { t[v] = y; return; }
  int tm = (tl + tr) / 2;
  if (pos <= tm) update(2 * v, tl, tm, pos, y);
  else update(2 * v + 1, tm + 1, tr, pos, y);
  t[v] = max(t[2 * v], t[2 * v + 1]);
}

// first index j in [l, r] (and inside [tl, tr]) with h[j] >= x, or -1
int first_at_least(int v, int tl, int tr, int l, int r, int x) {
  if (tr < l || r < tl || t[v] < x) return -1;
  if (tl == tr) return tl;
  int tm = (tl + tr) / 2;
  int res = first_at_least(2 * v, tl, tm, l, r, x);
  if (res != -1) return res;
  return first_at_least(2 * v + 1, tm + 1, tr, l, r, x);
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int q;
  cin >> n >> q;
  h.assign(n + 1, 0);
  t.assign(4 * n, 0);
  for (int i = 1; i <= n; i++) cin >> h[i];
  build(1, 1, n);
  string out;
  while (q--) {
    int type;
    cin >> type;
    if (type == 1) {
      int i, y;
      cin >> i >> y;
      update(1, 1, n, i, y);
    } else {
      int l, r, x;
      cin >> l >> r >> x;
      out += to_string(first_at_least(1, 1, n, l, r, x));
      out += '\n';
    }
  }
  cout << out;
}
