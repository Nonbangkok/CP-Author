// Reference for lp_dc02_twice_as_big: merge sort. Before merging two sorted
// halves, count the cross pairs with one pointer: for right elements in
// increasing order, 2 * a[j] only grows, so the first left element that is
// > 2 * a[j] only moves right. O(N log N).
#include <bits/stdc++.h>
using namespace std;

vector<long long> a, buf;

long long sortCount(int l, int r) {  // sorts a[l, r), returns pairs inside
  if (r - l <= 1) return 0;
  int m = (l + r) / 2;
  long long count = sortCount(l, m) + sortCount(m, r);
  int i = l;
  for (int j = m; j < r; j++) {
    while (i < m && a[i] <= 2 * a[j]) i++;
    count += m - i;  // a[i..m-1] are all > 2 * a[j]
  }
  merge(a.begin() + l, a.begin() + m, a.begin() + m, a.begin() + r, buf.begin() + l);
  copy(buf.begin() + l, buf.begin() + r, a.begin() + l);
  return count;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  a.resize(n);
  buf.resize(n);
  for (auto &v : a) cin >> v;
  cout << sortCount(0, n) << '\n';
}
