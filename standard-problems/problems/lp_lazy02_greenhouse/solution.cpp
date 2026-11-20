// Reference for lp_lazy02_greenhouse: lazy segment tree of maximums with two
// tags per node -- "set everything to S" (has_set, set_val) and "add A"
// (add_val). The pending work of a node always reads "first set (if any),
// then add": a new set wipes both, a new add joins whichever tag is there.
#include <bits/stdc++.h>
using namespace std;

int n;
vector<long long> a, mx, set_val, add_val;
vector<char> has_set;

void apply_set(int v, long long x) {
  mx[v] = x;
  has_set[v] = 1;
  set_val[v] = x;
  add_val[v] = 0;  // an older add is overwritten by the set
}

void apply_add(int v, long long x) {
  mx[v] += x;
  if (has_set[v]) set_val[v] += x;  // "set S then add x" is just "set S + x"
  else add_val[v] += x;
}

void push(int v) {
  if (has_set[v]) {
    apply_set(2 * v, set_val[v]);
    apply_set(2 * v + 1, set_val[v]);
    has_set[v] = 0;
  }
  if (add_val[v] != 0) {
    apply_add(2 * v, add_val[v]);
    apply_add(2 * v + 1, add_val[v]);
    add_val[v] = 0;
  }
}

void build(int v, int tl, int tr) {
  if (tl == tr) { mx[v] = a[tl]; return; }
  int tm = (tl + tr) / 2;
  build(2 * v, tl, tm);
  build(2 * v + 1, tm + 1, tr);
  mx[v] = max(mx[2 * v], mx[2 * v + 1]);
}

// type 1 = add x, type 2 = set to x
void update(int v, int tl, int tr, int l, int r, int type, long long x) {
  if (r < tl || tr < l) return;
  if (l <= tl && tr <= r) {
    if (type == 1) apply_add(v, x);
    else apply_set(v, x);
    return;
  }
  push(v);
  int tm = (tl + tr) / 2;
  update(2 * v, tl, tm, l, r, type, x);
  update(2 * v + 1, tm + 1, tr, l, r, type, x);
  mx[v] = max(mx[2 * v], mx[2 * v + 1]);
}

long long query(int v, int tl, int tr, int l, int r) {
  if (r < tl || tr < l) return LLONG_MIN;
  if (l <= tl && tr <= r) return mx[v];
  push(v);
  int tm = (tl + tr) / 2;
  return max(query(2 * v, tl, tm, l, r), query(2 * v + 1, tm + 1, tr, l, r));
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int q;
  cin >> n >> q;
  a.assign(n + 1, 0);
  mx.assign(4 * n, 0);
  set_val.assign(4 * n, 0);
  add_val.assign(4 * n, 0);
  has_set.assign(4 * n, 0);
  for (int i = 1; i <= n; i++) cin >> a[i];
  build(1, 1, n);
  string out;
  while (q--) {
    int type, l, r;
    cin >> type >> l >> r;
    if (type == 3) {
      out += to_string(query(1, 1, n, l, r));
      out += '\n';
    } else {
      long long v;
      cin >> v;
      update(1, 1, n, l, r, type, v);
    }
  }
  cout << out;
}
