// Naive O(N^2): extend every start until the sum reaches S. Correct, and must
// time out on the last subtask, whose first case needs half the array.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  long long s;
  cin >> n >> s;
  vector<long long> a(n);
  for (auto &x : a) cin >> x;
  int best = INT_MAX;
  for (int l = 0; l < n; l++) {
    long long sum = 0;
    for (int r = l; r < n; r++) {
      sum += a[r];
      if (sum >= s) {
        best = min(best, r - l + 1);
        break;
      }
    }
  }
  cout << (best == INT_MAX ? -1 : best) << '\n';
}
