// Reference for lp_dc01_taller_in_front: count inversions during merge sort.
// When the merge takes an element from the right half, every element still
// waiting in the left half is strictly larger and stands in front of it.
// O(N log N).
#include <bits/stdc++.h>
using namespace std;

vector<long long> a, buf;

long long sortCount(int l, int r) {  // sorts a[l, r), returns inversions inside
  if (r - l <= 1) return 0;
  int m = (l + r) / 2;
  long long count = sortCount(l, m) + sortCount(m, r);
  int i = l, j = m, k = l;
  while (i < m || j < r) {
    if (j == r || (i < m && a[i] <= a[j])) {
      buf[k++] = a[i++];
    } else {
      count += m - i;  // a[i..m-1] are all > a[j]
      buf[k++] = a[j++];
    }
  }
  for (int t = l; t < r; t++) a[t] = buf[t];
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
