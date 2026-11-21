// Naive: try d = 1, 2, 3, ... until the greedy check fails. Correct, but the
// answer can be close to 10^9, so it must time out on the last subtask.
#include <bits/stdc++.h>
using namespace std;

int n, k;
vector<long long> x;

bool ok(long long d) {
  int placed = 1;
  long long last = x[0];
  for (int i = 1; i < n && placed < k; i++)
    if (x[i] - last >= d) {
      placed++;
      last = x[i];
    }
  return placed >= k;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  cin >> n >> k;
  x.resize(n);
  for (long long &v : x) cin >> v;
  sort(x.begin(), x.end());
  long long d = 1;
  while (ok(d + 1)) d++;
  cout << d << '\n';
}
