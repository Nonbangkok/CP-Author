// Reference for lp_bsx02_split_work: binary search on the answer S.
// ok(S) = greedily cutting a new part whenever the sum would exceed S needs
// at most K parts; ok is false ... false true ... true, find the first true.
// O(N log(sum)).
#include <bits/stdc++.h>
using namespace std;

int n, k;
vector<long long> a;

bool ok(long long cap) {
  int parts = 1;
  long long current = 0;
  for (long long v : a) {
    if (v > cap) return false;
    if (current + v > cap) {
      parts++;
      current = 0;
    }
    current += v;
  }
  return parts <= k;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  cin >> n >> k;
  a.resize(n);
  long long total = 0;
  for (long long &v : a) {
    cin >> v;
    total += v;
  }
  long long lo = 0, hi = total;  // ok(lo) is false, ok(hi) is true
  while (hi - lo > 1) {
    long long mid = lo + (hi - lo) / 2;
    if (ok(mid)) hi = mid;
    else lo = mid;
  }
  cout << hi << '\n';
}
