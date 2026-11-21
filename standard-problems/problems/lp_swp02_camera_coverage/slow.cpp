// Naive O(N^2): cut the line at every endpoint, and for every elementary piece
// count the cameras that cover it by scanning all of them. Correct, must time
// out on the last subtask.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<long long> l(n), r(n), xs;
  for (int i = 0; i < n; i++) {
    cin >> l[i] >> r[i];
    xs.push_back(l[i]);
    xs.push_back(r[i]);
  }
  sort(xs.begin(), xs.end());
  xs.erase(unique(xs.begin(), xs.end()), xs.end());
  vector<long long> atLeast(n + 2, 0);
  for (size_t p = 0; p + 1 < xs.size(); p++) {
    int c = 0;
    for (int i = 0; i < n; i++)
      if (l[i] <= xs[p] && xs[p + 1] <= r[i]) c++;
    for (int k = 1; k <= c; k++) atLeast[k] += xs[p + 1] - xs[p];
  }
  for (int k = 1; k <= n; k++) cout << atLeast[k] << (k < n ? ' ' : '\n');
}
