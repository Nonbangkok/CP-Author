// Reference for lp_cx01_distinct_values: sort, then count the positions where
// the value changes, O(N log N).
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> a(n);
  for (int &x : a) cin >> x;
  sort(a.begin(), a.end());
  int distinct = 0;
  for (int i = 0; i < n; i++)
    if (i == 0 || a[i] != a[i - 1]) distinct++;
  cout << distinct << '\n';
}
