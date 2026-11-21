// Reference for lp_bsa03_pair_budget: sort, then for every j count the i < j
// with a[i] <= K - a[j] by upper_bound on the prefix, O(N log N).
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  long long k;
  cin >> n >> k;
  vector<long long> a(n);
  for (long long &v : a) cin >> v;
  sort(a.begin(), a.end());
  long long pairs = 0;
  for (int j = 0; j < n; j++)
    pairs += upper_bound(a.begin(), a.begin() + j, k - a[j]) - a.begin();
  cout << pairs << '\n';
}
