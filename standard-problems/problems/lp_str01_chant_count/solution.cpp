// Reference for lp_str01_chant_count: KMP. The prefix function of P tells, after
// a mismatch, the longest border to fall back to, so the scan over T never moves
// backwards. Overlapping occurrences: after a full match fall back to pi[m-1].
// O(|T| + |P|).
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string t, p;
  cin >> t >> p;
  int n = t.size(), m = p.size();
  vector<int> pi(m, 0);
  for (int i = 1; i < m; i++) {
    int k = pi[i - 1];
    while (k > 0 && p[i] != p[k]) k = pi[k - 1];
    if (p[i] == p[k]) k++;
    pi[i] = k;
  }
  long long count = 0;
  int k = 0;  // letters of P matched so far
  for (int i = 0; i < n; i++) {
    while (k > 0 && t[i] != p[k]) k = pi[k - 1];
    if (t[i] == p[k]) k++;
    if (k == m) {
      count++;
      k = pi[m - 1];
    }
  }
  cout << count << '\n';
}
