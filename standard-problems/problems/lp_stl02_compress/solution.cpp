// Reference for lp_stl02_compress: sort + unique + erase builds the sorted
// distinct values, then lower_bound finds each rank, O(N log N).
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> a(n);
  for (int &x : a) cin >> x;
  vector<int> v = a;
  sort(v.begin(), v.end());
  v.erase(unique(v.begin(), v.end()), v.end());
  cout << v.size() << '\n';
  for (int i = 0; i < n; i++) {
    if (i) cout << ' ';
    cout << lower_bound(v.begin(), v.end(), a[i]) - v.begin() + 1;
  }
  cout << '\n';
}
