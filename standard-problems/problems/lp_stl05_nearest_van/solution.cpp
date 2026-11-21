// Reference for lp_stl05_nearest_van: a multiset; erase ONE copy through
// find(), answer with lower_bound and its predecessor, O(log Q) per command.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int q;
  cin >> q;
  multiset<long long> s;
  while (q--) {
    int t;
    long long x;
    cin >> t >> x;
    if (t == 1) {
      s.insert(x);
    } else if (t == 2) {
      s.erase(s.find(x));
    } else if (s.empty()) {
      cout << -1 << '\n';
    } else {
      auto it = s.lower_bound(x);  // first value >= x
      long long best = -1;
      if (it != s.end()) best = *it;
      if (it != s.begin()) {
        long long below = *prev(it);
        if (best == -1 || x - below <= best - x) best = below;  // tie -> smaller
      }
      cout << best << '\n';
    }
  }
}
