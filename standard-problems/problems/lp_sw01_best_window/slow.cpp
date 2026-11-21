// Naive O(NK): add up every window from scratch. Correct, and must time out
// on the last subtask, whose first case has K = N / 2.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, k;
  cin >> n >> k;
  vector<long long> a(n);
  for (auto &x : a) cin >> x;
  long long best = LLONG_MIN;
  for (int i = 0; i + k <= n; i++) {
    long long sum = 0;
    for (int j = i; j < i + k; j++) sum += a[j];
    best = max(best, sum);
  }
  cout << best << '\n';
}
