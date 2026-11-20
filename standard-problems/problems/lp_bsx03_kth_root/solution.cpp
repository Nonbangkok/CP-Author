// Reference for lp_bsx03_kth_root: binary search the last x with x^k <= n.
// power() stops as soon as the product would pass n, so it never overflows.
#include <bits/stdc++.h>
using namespace std;

// x^k if it is <= n, otherwise n + 1 (any value > n would do).
long long power(long long x, int k, long long n) {
  long long r = 1;
  for (int i = 0; i < k; i++) {
    if (r > n / x) return n + 1;
    r *= x;
  }
  return r;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int q;
  cin >> q;
  while (q--) {
    long long n;
    int k;
    cin >> n >> k;
    long long lo = 1, hi = 1000000001;  // 1^k <= n always; (10^9 + 1)^2 > 10^18
    while (hi - lo > 1) {
      long long mid = lo + (hi - lo) / 2;
      if (power(mid, k, n) <= n) lo = mid;
      else hi = mid;
    }
    cout << lo << '\n';
  }
}
