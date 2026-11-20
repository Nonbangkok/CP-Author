// Naive O(N^2) DP: sort by end, best[i] = most bookings among the first i+1
// that may end with booking i, scanning every earlier booking for the best
// compatible one. Correct, and must time out on the last subtask.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  long long c;
  cin >> n >> c;
  vector<pair<long long, long long>> b(n);  // (end, start)
  for (auto &[e, s] : b) {
    long long d;
    cin >> s >> d;
    e = s + d;
  }
  sort(b.begin(), b.end());
  vector<int> best(n);
  int answer = 0;
  for (int i = 0; i < n; i++) {
    int before = 0;
    for (int j = 0; j < i; j++)
      if (b[j].first + c <= b[i].second) before = max(before, best[j]);
    best[i] = before + 1;
    answer = max(answer, best[i]);
  }
  cout << answer << '\n';
}
