// Naive O(N^2): from every start, extend until a (K+1)-th flavour appears.
// "seen[v] == l" marks the flavours met from the current start, so nothing
// needs clearing between starts. Correct, and must time out on the last subtask.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, k;
  cin >> n >> k;
  vector<int> a(n);
  for (int &x : a) cin >> x;
  vector<int> sorted_values(a);
  sort(sorted_values.begin(), sorted_values.end());
  sorted_values.erase(unique(sorted_values.begin(), sorted_values.end()), sorted_values.end());
  for (int &x : a) x = lower_bound(sorted_values.begin(), sorted_values.end(), x) - sorted_values.begin();

  vector<int> seen(sorted_values.size(), -1);
  int best = 0;
  for (int l = 0; l < n; l++) {
    int distinct = 0, r = l;
    while (r < n) {
      if (seen[a[r]] != l) {
        if (distinct == k) break;
        seen[a[r]] = l;
        distinct++;
      }
      r++;
    }
    best = max(best, r - l);
  }
  cout << best << '\n';
}
