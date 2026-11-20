// Reference for lp_gs03_mod_product: reduce every a_i modulo P first, then
// keep both running values below P, so every product fits in long long.
#include <bits/stdc++.h>
using namespace std;

const long long MOD = 1000000007LL;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  long long sum = 0, product = 1;
  for (int i = 0; i < n; i++) {
    long long x;
    cin >> x;
    x %= MOD;
    sum = (sum + x) % MOD;
    product = product * x % MOD;
  }
  cout << sum << '\n' << product << '\n';
}
