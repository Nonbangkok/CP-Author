// Naive: try every route by plain recursion, no memo. best(i) recomputes the
// same stones again and again, so the work grows exponentially with N.
// Correct, and must time out on the last subtask. Depth <= N <= 2 * 10^4.
#include <bits/stdc++.h>
using namespace std;

int n, k;
vector<long long> h;

long long best(int i) {  // least effort from stone i to stone n - 1
  if (i == n - 1) return 0;
  long long result = LLONG_MAX;
  for (int d = 1; d <= k && i + d < n; d++)
    result = min(result, llabs(h[i] - h[i + d]) + best(i + d));
  return result;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  cin >> n >> k;
  h.resize(n);
  for (long long &x : h) cin >> x;
  cout << best(0) << '\n';
}
