// Naive O(N Q): keep the plain array, set in O(1), and add the shelves one by
// one for every question. Correct, and must time out on the last subtask.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, q;
  cin >> n >> q;
  vector<long long> a(n + 1);
  for (int i = 1; i <= n; i++) cin >> a[i];
  while (q--) {
    int type;
    cin >> type;
    if (type == 1) {
      int i;
      long long x;
      cin >> i >> x;
      a[i] = x;
    } else {
      int l, r;
      cin >> l >> r;
      long long s = 0;
      for (int k = l; k <= r; k++) s += a[k];
      cout << s << '\n';
    }
  }
}
