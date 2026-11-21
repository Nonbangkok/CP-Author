// Reference for lp_tp01_swan_boats: greedy + two pointers from opposite ends, O(N).
// The heaviest person left must take some boat; if anyone at all can share it
// with them, the lightest person can, and giving them the lightest is never
// worse. So: pair a[l] with a[r] when it fits, otherwise a[r] goes alone.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  long long k;
  cin >> n >> k;
  vector<long long> a(n);
  for (auto &x : a) cin >> x;
  int boats = 0;
  int l = 0, r = n - 1;
  while (l <= r) {  // l == r: one person left, who goes alone
    if (l < r && a[l] + a[r] <= k) l++;
    r--;
    boats++;
  }
  cout << boats << '\n';
}
