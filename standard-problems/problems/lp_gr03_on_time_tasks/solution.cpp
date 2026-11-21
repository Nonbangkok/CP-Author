// Reference for lp_gr03_on_time_tasks (Moore-Hodgson): go through the tasks by
// deadline, add each one; if the total time now passes this deadline, drop the
// longest task chosen so far (max-heap). O(N log N).
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
  priority_queue<long long> chosen;
  long long total = 0;  // up to 2 * 10^9 just before a drop: needs 64 bits
  for (auto &[d, t] : tasks) {
    chosen.push(t);
    total += t;
    if (total > d) {
      total -= chosen.top();
      chosen.pop();
    }
  }
  cout << chosen.size() << '\n';
}
