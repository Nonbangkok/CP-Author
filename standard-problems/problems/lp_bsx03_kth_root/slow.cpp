// Naive: x = 1, 2, 3, ... while (x + 1)^k <= n. Correct (same overflow-safe
// power), but the answer reaches 10^9 for k = 2: times out on the last subtask.
#include <bits/stdc++.h>
using namespace std;

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
    long long x = 1;
    while (power(x + 1, k, n) <= n) x++;
    cout << x << '\n';
  }
}
