// Reference for lp_dp03_lakeside_stalls: break the circle by cases.
// Spot 1 and spot N are neighbours, so at least one of them is unused:
// answer = max(best on a[1..N-1], best on a[2..N]), each a straight line.
// Line DP: take = best with the current spot used, skip = best without it.
// O(N); sums reach 5 * 10^13, so long long.
#include <bits/stdc++.h>
using namespace std;

long long line(const vector<long long> &a, int from, int to) {  // a[from .. to - 1]
  long long take = 0, skip = 0;
  for (int i = from; i < to; i++) {
    long long new_take = skip + a[i];
    long long new_skip = max(take, skip);
    take = new_take;
    skip = new_skip;
  }
  return max(take, skip);
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<long long> a(n);
  for (long long &x : a) cin >> x;
  cout << max(line(a, 0, n - 1), line(a, 1, n)) << '\n';
}
