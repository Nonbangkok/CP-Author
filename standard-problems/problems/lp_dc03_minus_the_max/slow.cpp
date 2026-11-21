// Naive O(N^2): from every start, extend to the right keeping the sum and the
// maximum. Correct, must time out on the last subtask.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<long long> a(n);
  for (auto &v : a) cin >> v;
  long long best = 0;
  for (int l = 0; l < n; l++) {
    long long sum = 0, mx = a[l];
    for (int r = l; r < n; r++) {
      sum += a[r];
      mx = max(mx, a[r]);
      best = max(best, sum - mx);
    }
  }
  cout << best << '\n';
}
