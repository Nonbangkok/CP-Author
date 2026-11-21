// Naive O(N^2): the same greedy, but the lightest person still on the shore is
// found by scanning from the left every time. Correct, and must time out on the
// last subtask, whose first case pairs up almost everyone.
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
  vector<char> used(n, 0);
  int boats = 0;
  for (int r = n - 1; r >= 0; r--) {
    if (used[r]) continue;
    used[r] = 1;
    boats++;
    int lightest = -1;
    for (int i = 0; i < r; i++)
      if (!used[i]) { lightest = i; break; }
    if (lightest != -1 && a[lightest] + a[r] <= k) used[lightest] = 1;
  }
  cout << boats << '\n';
}
