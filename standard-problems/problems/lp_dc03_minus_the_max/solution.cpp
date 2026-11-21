// Reference for lp_dc03_minus_the_max: divide and conquer on the array.
// The best block lies in the left half, in the right half, or crosses the
// middle. A crossing block = a suffix of the left half (length kl) + a prefix
// of the right half (length kr), worth SL + SR - max(ML, MR). Go through kl in
// increasing order: ML only grows, so the right prefixes with MR <= ML are
// 1..p with p only moving right. For kr <= p the value is SL - ML + SR (best SR
// from a prefix max), for kr > p it is SL + (SR - MR) (from a suffix max).
// O(n) per level, O(N log N) in all.
#include <bits/stdc++.h>
using namespace std;

const long long NEG = LLONG_MIN / 4;
vector<long long> a;

long long solve(int l, int r) {  // best value of a block inside a[l, r)
  if (r - l == 1) return 0;      // one card: the friend takes it
  int m = (l + r) / 2;
  long long best = max(solve(l, m), solve(m, r));

  int nl = m - l, nr = r - m;
  vector<long long> sl(nl + 1), ml(nl + 1), sr(nr + 2), mr(nr + 2), pm(nr + 1), sm(nr + 2);
  for (int k = 1; k <= nl; k++) {  // suffix a[m-k, m)
    sl[k] = sl[k - 1] + a[m - k];
    ml[k] = (k == 1) ? a[m - 1] : max(ml[k - 1], a[m - k]);
  }
  for (int k = 1; k <= nr; k++) {  // prefix a[m, m+k)
    sr[k] = sr[k - 1] + a[m + k - 1];
    mr[k] = (k == 1) ? a[m] : max(mr[k - 1], a[m + k - 1]);
  }
  pm[0] = NEG;
  for (int k = 1; k <= nr; k++) pm[k] = max(pm[k - 1], sr[k]);
  sm[nr + 1] = NEG;
  for (int k = nr; k >= 1; k--) sm[k] = max(sm[k + 1], sr[k] - mr[k]);

  int p = 0;
  for (int k = 1; k <= nl; k++) {
    while (p < nr && mr[p + 1] <= ml[k]) p++;
    if (p >= 1) best = max(best, sl[k] - ml[k] + pm[p]);  // the max is on the left
    if (p < nr) best = max(best, sl[k] + sm[p + 1]);      // the max is on the right
  }
  return best;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  a.resize(n);
  for (auto &v : a) cin >> v;
  cout << solve(0, n) << '\n';
}
