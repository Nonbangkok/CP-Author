// Naive O(NQ) scan: correct, and must time out on the last subtask.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, q;
  cin >> n >> q;
  vector<long long> a(n);
  for (long long &v : a) cin >> v;
  while (q--) {
    long long x;
    cin >> x;
    long long best = a[0];
    for (long long v : a) {
      long long d = llabs(v - x), bd = llabs(best - x);
      if (d < bd || (d == bd && v < best)) best = v;
    }
    cout << best << '\n';
  }
}
