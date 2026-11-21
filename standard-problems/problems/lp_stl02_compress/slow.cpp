// Naive O(N * D): linear search to collect distinct values and again to find
// each rank. Correct, and must time out on the last subtask.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> a(n);
  for (int &x : a) cin >> x;
  vector<int> v;
  for (int x : a) {
    bool found = false;
    for (int y : v)
      if (y == x) { found = true; break; }
    if (!found) v.push_back(x);
  }
  sort(v.begin(), v.end());
  cout << v.size() << '\n';
  for (int i = 0; i < n; i++) {
    int rank = 0;
    while (v[rank] != a[i]) rank++;
    if (i) cout << ' ';
    cout << rank + 1;
  }
  cout << '\n';
}
