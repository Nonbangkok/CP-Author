// Naive O(N^2): extend every start until the budget breaks. Correct, and must
// time out on the last subtask, whose first case lets most subarrays fit.
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
  long long count = 0;
  for (int l = 0; l < n; l++) {
    long long sum = 0;
    for (int r = l; r < n; r++) {
      sum += a[r];
      if (sum > s) break;
      count++;
    }
  }
  cout << count << '\n';
}
