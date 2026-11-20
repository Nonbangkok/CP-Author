// Naive: walk the recurrence one day at a time. O(N) -- fine up to 10^7,
// hopeless for N ~ 10^18 on the last subtask.
#include <bits/stdc++.h>
using namespace std;

const long long MOD = 1000000007LL;

int main() {
  long long a, b, c, f0, f1, n;
  cin >> a >> b >> c >> f0 >> f1 >> n;
  long long prev = f0 % MOD, cur = f1 % MOD;
  if (n == 0) {
    cout << prev << '\n';
    return 0;
  }
  for (long long day = 2; day <= n; day++) {
    long long next = (a * cur % MOD + b * prev % MOD + c) % MOD;
    prev = cur;
    cur = next;
  }
  cout << cur << '\n';
}
