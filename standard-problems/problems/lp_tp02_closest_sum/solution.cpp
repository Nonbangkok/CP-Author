// Reference for lp_tp02_closest_sum: sort, then two pointers from opposite
// ends, O(N log N). A sum below T can only grow by moving l right; a sum above
// T can only shrink by moving r left; each step discards one element for good.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  long long t;
  cin >> n >> t;
  vector<long long> a(n);
  for (auto &x : a) cin >> x;
  sort(a.begin(), a.end());
  long long best = LLONG_MAX;
  int l = 0, r = n - 1;
  while (l < r) {
    long long sum = a[l] + a[r];
    best = min(best, llabs(sum - t));
    if (sum < t) l++;
    else if (sum > t) r--;
    else break;  // exact hit, cannot do better than 0
  }
  cout << best << '\n';
}
