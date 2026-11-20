// Reference for lp_rec01_subset_sum: include/exclude recursion over all
// 2^N subsets, O(2^N).
#include <bits/stdc++.h>
using namespace std;

int n;
long long target;
vector<long long> a;

long long countWays(int i, long long sum) {
  if (i == n) return sum == target ? 1 : 0;
  return countWays(i + 1, sum + a[i]) + countWays(i + 1, sum);
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  cin >> n >> target;
  a.resize(n);
  for (long long &x : a) cin >> x;
  cout << countWays(0, 0) << '\n';
}
