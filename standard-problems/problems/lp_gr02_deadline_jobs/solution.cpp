// Reference for lp_gr02_deadline_jobs: go through the jobs by deadline and keep
// the chosen profits in a min-heap. After the jobs with deadline <= d are in,
// at most d of them fit, so while the heap is bigger than d drop the smallest
// profit (exchange argument). O(N log N).
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<pair<long long, long long>> jobs(n);  // (deadline, profit)
  for (auto &[d, p] : jobs) cin >> d >> p;
  sort(jobs.begin(), jobs.end());
  priority_queue<long long, vector<long long>, greater<long long>> chosen;
  long long total = 0;
  for (auto &[d, p] : jobs) {
    chosen.push(p);
    total += p;
    if ((long long)chosen.size() > d) {
      total -= chosen.top();
      chosen.pop();
    }
  }
  cout << total << '\n';
}
