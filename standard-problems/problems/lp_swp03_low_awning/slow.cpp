// Naive O(N * Q): for every truck, look at every awning. Correct, must time
// out on the last subtask.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, q;
  cin >> n >> q;
  vector<long long> l(n), r(n), h(n);
  for (int i = 0; i < n; i++) cin >> l[i] >> r[i] >> h[i];
  for (int j = 0; j < q; j++) {
    long long p;
    cin >> p;
    long long best = -1;
    for (int i = 0; i < n; i++)
      if (l[i] <= p && p <= r[i] && (best == -1 || h[i] < best)) best = h[i];
    cout << best << '\n';
  }
}
