// Reference for lp_bexp02_geometric_sum: walk the bits of the term count
// n + 1 from the top, keeping (S, P) = (1 + a + ... + a^(k-1), a^k) mod m.
// k -> 2k:  S = S * (1 + P), P = P * P.   k -> k + 1:  S = S + P, P = P * a.
// O(log n) per query, no division, so any m works.
#include <bits/stdc++.h>
using namespace std;

long long geometric(long long a, long long n, long long m) {
  a %= m;
  unsigned long long terms = (unsigned long long)n + 1;
  long long s = 0, p = 1 % m;
  for (int bit = 63; bit >= 0; bit--) {
    s = s * ((1 + p) % m) % m;
    p = p * p % m;
    if ((terms >> bit) & 1) {
      s = (s + p) % m;
      p = p * a % m;
    }
  }
  return s;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int q;
  cin >> q;
  while (q--) {
    long long a, n, m;
    cin >> a >> n >> m;
    cout << geometric(a, n, m) << '\n';
  }
}
