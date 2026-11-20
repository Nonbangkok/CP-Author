// Reference for lp_fw03_bird_species: offline distinct count with a Fenwick
// tree, O((N + Q) log N). Answer the questions sorted by r; while sweeping r,
// keep a 1 only at the LAST position seen so far of every species (move it
// when the species appears again). Then the answer for [l, r] is the number of
// ones in [l, r]: a species occurs in [l, r] exactly when its last occurrence
// up to r is >= l. Species go up to 10^9, so they are renumbered first.
#include <bits/stdc++.h>
using namespace std;

int n;
vector<int> bit;

void add(int i, int delta) {
  for (; i <= n; i += i & -i) bit[i] += delta;
}

int prefix(int i) {
  int s = 0;
  for (; i > 0; i -= i & -i) s += bit[i];
  return s;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int q;
  cin >> n >> q;
  vector<int> a(n + 1);
  for (int i = 1; i <= n; i++) cin >> a[i];
  vector<int> vals(a.begin() + 1, a.end());
  sort(vals.begin(), vals.end());
  vals.erase(unique(vals.begin(), vals.end()), vals.end());
  for (int i = 1; i <= n; i++) a[i] = lower_bound(vals.begin(), vals.end(), a[i]) - vals.begin();

  vector<int> ql(q), qr(q), order(q);
  for (int j = 0; j < q; j++) cin >> ql[j] >> qr[j];
  iota(order.begin(), order.end(), 0);
  sort(order.begin(), order.end(), [&](int x, int y) { return qr[x] < qr[y]; });

  bit.assign(n + 1, 0);
  vector<int> last(vals.size(), 0);  // 0 = not seen yet
  vector<int> answer(q);
  int r = 0;
  for (int j : order) {
    while (r < qr[j]) {
      r++;
      if (last[a[r]] != 0) add(last[a[r]], -1);
      last[a[r]] = r;
      add(r, 1);
    }
    answer[j] = prefix(qr[j]) - prefix(ql[j] - 1);
  }
  for (int j = 0; j < q; j++) cout << answer[j] << '\n';
}
