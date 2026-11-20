// Naive O(N^2): try every pair. Correct, and must time out on the last subtask.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  long long t;
  cin >> n >> t;
  vector<long long> a(n);
  for (auto &x : a) cin >> x;
  long long best = LLONG_MAX;
  for (int i = 0; i < n; i++)
    for (int j = i + 1; j < n; j++)
      best = min(best, llabs(a[i] + a[j] - t));
  cout << best << '\n';
}
