// Naive: try all 2^N subsets by recursion (take item i or not) and keep the
// most valuable one that fits. Correct, and must time out on the last
// subtask. (The textbook capacity-indexed knapsack would need an array of
// W + 1 = 10^9 + 1 entries, which does not fit in memory either.)
#include <bits/stdc++.h>
using namespace std;

int n;
long long cap;
vector<long long> w;
vector<int> v;
int best = 0;

void pick(int i, long long weight, int value) {
  if (weight > cap) return;
  if (i == n) {
    best = max(best, value);
    return;
  }
  pick(i + 1, weight, value);
  pick(i + 1, weight + w[i], value + v[i]);
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  cin >> n >> cap;
  w.resize(n);
  v.resize(n);
  for (int i = 0; i < n; i++) cin >> w[i] >> v[i];
  pick(0, 0, 0);
  cout << best << '\n';
}
