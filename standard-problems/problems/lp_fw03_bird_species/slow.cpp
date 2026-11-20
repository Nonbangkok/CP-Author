// Naive O(N Q): for every question walk l..r and count species not met yet in
// this question (seen[v] == j marks them, so nothing is cleared between
// questions). Correct, and must time out on the last subtask.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, q;
  cin >> n >> q;
  vector<int> a(n + 1);
  for (int i = 1; i <= n; i++) cin >> a[i];
  vector<int> vals(a.begin() + 1, a.end());
  sort(vals.begin(), vals.end());
  vals.erase(unique(vals.begin(), vals.end()), vals.end());
  for (int i = 1; i <= n; i++) a[i] = lower_bound(vals.begin(), vals.end(), a[i]) - vals.begin();

  vector<int> seen(vals.size(), -1);
  for (int j = 0; j < q; j++) {
    int l, r;
    cin >> l >> r;
    int distinct = 0;
    for (int k = l; k <= r; k++) {
      if (seen[a[k]] != j) {
        seen[a[k]] = j;
        distinct++;
      }
    }
    cout << distinct << '\n';
  }
}
