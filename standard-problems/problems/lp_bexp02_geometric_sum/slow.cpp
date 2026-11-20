// Naive O(n) per query: add the n + 1 terms one by one.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int q;
  cin >> q;
  while (q--) {
    long long a, n, m;
    cin >> a >> n >> m;
    a %= m;
    long long sum = 0, term = 1 % m;
    for (long long i = 0; i <= n; i++) {
      sum = (sum + term) % m;
      term = term * a % m;
    }
    cout << sum << '\n';
  }
}
