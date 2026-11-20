// Naive O(b) per query: multiply b times. Correct, and must time out once b is huge.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int q;
  cin >> q;
  while (q--) {
    long long a, b, m;
    cin >> a >> b >> m;
    a %= m;
    long long result = 1 % m;
    for (long long i = 0; i < b; i++) result = result * a % m;
    cout << result << '\n';
  }
}
