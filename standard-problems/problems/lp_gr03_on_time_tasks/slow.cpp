// Naive O(N^2) DP over the tasks sorted by deadline (any on-time set can be
// done in deadline order): least[k] = least total time of k on-time tasks
// chosen so far. Correct, and must time out on the last subtask.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<pair<long long, long long>> tasks(n);  // (deadline, duration)
  for (auto &[d, t] : tasks) cin >> t >> d;
  sort(tasks.begin(), tasks.end());
  const long long INF = LLONG_MAX / 4;
  vector<long long> least(n + 1, INF);
  least[0] = 0;
  for (int i = 0; i < n; i++) {
    auto [d, t] = tasks[i];
    for (int k = i + 1; k >= 1; k--)
      if (least[k - 1] + t <= d) least[k] = min(least[k], least[k - 1] + t);
  }
  int best = 0;
  for (int k = 0; k <= n; k++)
    if (least[k] < INF) best = k;
  cout << best << '\n';
}
