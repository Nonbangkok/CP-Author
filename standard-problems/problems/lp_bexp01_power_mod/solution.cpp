// Reference for lp_bexp01_power_mod: iterative binary exponentiation,
// O(log b) per query. a is reduced mod m first so every product fits in long long.
#include <bits/stdc++.h>
using namespace std;

long long power(long long a, long long b, long long m) {
  long long result = 1 % m;
  a %= m;
  while (b > 0) {
    if (b & 1) result = result * a % m;
    a = a * a % m;
    b >>= 1;
  }
  return result;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int q;
  cin >> q;
  while (q--) {
    long long a, b, m;
    cin >> a >> b >> m;
    cout << power(a, b, m) << '\n';
  }
}
