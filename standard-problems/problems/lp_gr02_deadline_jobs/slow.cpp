// Naive: take jobs from the most profitable down and give each the latest free
// day <= its deadline, scanning the days one by one. Correct, but with large
// deadlines every job scans past all the days already taken: O(N^2).
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<pair<long long, long long>> jobs(n);  // (profit, deadline)
  for (auto &[p, d] : jobs) cin >> d >> p;
  sort(jobs.rbegin(), jobs.rend());
  vector<bool> used(n + 1, false);  // days 1..n are enough: at most n jobs
  long long total = 0;
  for (auto &[p, d] : jobs) {
    for (long long day = min<long long>(d, n); day >= 1; day--) {
      if (!used[day]) {
        used[day] = true;
        total += p;
        break;
      }
    }
  }
  cout << total << '\n';
}
