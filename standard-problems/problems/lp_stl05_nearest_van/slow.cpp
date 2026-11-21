// Naive O(Q) per command: an unsorted vector, linear scans for erase and for
// the closest value. Correct, and must time out on the last subtask.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int q;
  cin >> q;
  vector<long long> a;
  while (q--) {
    int t;
    long long x;
    cin >> t >> x;
    if (t == 1) {
      a.push_back(x);
    } else if (t == 2) {
      for (size_t i = 0; i < a.size(); i++)
        if (a[i] == x) {
          a[i] = a.back();
          a.pop_back();
          break;
        }
    } else {
      long long best = -1;
      for (long long v : a) {
        long long d = llabs(v - x), bd = llabs(best - x);
        if (best == -1 || d < bd || (d == bd && v < best)) best = v;
      }
      cout << best << '\n';
    }
  }
}
