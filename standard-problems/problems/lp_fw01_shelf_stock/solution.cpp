// Reference for lp_fw01_shelf_stock: Fenwick tree (point add, prefix sum),
// O((N + Q) log N). "Set shelf i to x" becomes "add x - a[i]", so the plain
// array a[] is kept next to the tree to know the old value. Sums reach
// 5 * 10^4 * 10^6 = 5 * 10^10, so they are long long.
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
  bit.assign(n + 1, 0);
  for (int i = 1; i <= n; i++) {
    cin >> a[i];
    add(i, a[i]);
  }
  while (q--) {
    int type;
    cin >> type;
    if (type == 1) {
      int i;
      long long x;
      cin >> i >> x;
      add(i, x - a[i]);
      a[i] = x;
    } else {
      int l, r;
      cin >> l >> r;
      cout << prefix(r) - prefix(l - 1) << '\n';
    }
  }
}
