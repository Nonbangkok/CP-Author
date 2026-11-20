// Naive O(N^2): every block of consecutive buildings l..r, with a running
// minimum height and running width. Correct, must time out on the last subtask.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<long long> w(n), h(n);
  for (int i = 0; i < n; i++) cin >> w[i] >> h[i];
  long long best = 0;
  for (int l = 0; l < n; l++) {
    long long low = h[l], width = 0;
    for (int r = l; r < n; r++) {
      low = min(low, h[r]);
      width += w[r];
      best = max(best, low * width);
    }
  }
  cout << best << '\n';
}
