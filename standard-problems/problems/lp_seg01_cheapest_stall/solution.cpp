// Reference for lp_seg01_cheapest_stall: recursive segment tree of minimums
// over [1, N] in a 4N array; point assignment and range minimum, O(log N) each.
#include <bits/stdc++.h>
using namespace std;

const int INF = INT_MAX;  // identity of min: never smaller than a real price
int n;
vector<int> a, t;

void build(int v, int tl, int tr) {
  if (tl == tr) { t[v] = a[tl]; return; }
  int tm = (tl + tr) / 2;
  build(2 * v, tl, tm);
  build(2 * v + 1, tm + 1, tr);
  t[v] = min(t[2 * v], t[2 * v + 1]);
}

void update(int v, int tl, int tr, int pos, int x) {
  if (tl == tr) { t[v] = x; return; }
  int tm = (tl + tr) / 2;
  if (pos <= tm) update(2 * v, tl, tm, pos, x);
  else update(2 * v + 1, tm + 1, tr, pos, x);
  t[v] = min(t[2 * v], t[2 * v + 1]);
}

int query(int v, int tl, int tr, int l, int r) {
  if (r < tl || tr < l) return INF;
  if (l <= tl && tr <= r) return t[v];
  int tm = (tl + tr) / 2;
  return min(query(2 * v, tl, tm, l, r), query(2 * v + 1, tm + 1, tr, l, r));
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int q;
  cin >> n >> q;
  a.assign(n + 1, 0);
  t.assign(4 * n, 0);
  for (int i = 1; i <= n; i++) cin >> a[i];
  build(1, 1, n);
  string out;
  while (q--) {
    int type, x, y;
    cin >> type >> x >> y;
    if (type == 1) update(1, 1, n, x, y);
    else { out += to_string(query(1, 1, n, x, y)); out += '\n'; }
  }
  cout << out;
}
