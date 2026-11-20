// Reference for lp_stl04_seen_before: map<string, int> counts as we go,
// O(N log N) string comparisons.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  map<string, int> cnt;
  string w;
  for (int i = 0; i < n; i++) {
    cin >> w;
    cout << ++cnt[w] << '\n';
  }
}
