// Reference for lp_dpk03_heavy_treasures: weights are huge, values are small,
// so index the knapsack by VALUE. minw[s] = least total weight of a subset
// worth exactly s (INF if none). 0/1 items: s goes downward, like the classic
// capacity loop. Answer = largest s with minw[s] <= W. O(N * sum v).
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  long long cap;
  cin >> n >> cap;
  vector<long long> w(n);
  vector<int> v(n);
  int total = 0;
  for (int i = 0; i < n; i++) {
    cin >> w[i] >> v[i];
    total += v[i];
  }
  const long long INF = LLONG_MAX / 2;
  vector<long long> minw(total + 1, INF);
  minw[0] = 0;
  int reach = 0;  // values above the sum of the items so far are still INF
  for (int i = 0; i < n; i++) {
    reach += v[i];
    for (int s = reach; s >= v[i]; s--)
      if (minw[s - v[i]] + w[i] < minw[s]) minw[s] = minw[s - v[i]] + w[i];
  }
  int best = 0;
  for (int s = 0; s <= total; s++)
    if (minw[s] <= cap) best = s;
  cout << best << '\n';
}
