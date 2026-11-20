// Naive: try every start and compare letter by letter (stop at the first
// mismatch). O(|T| * |P|) when almost every start matches for a long time.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string t, p;
  cin >> t >> p;
  int n = t.size(), m = p.size();
  long long count = 0;
  for (int i = 0; i + m <= n; i++) {
    int k = 0;
    while (k < m && t[i + k] == p[k]) k++;
    if (k == m) count++;
  }
  cout << count << '\n';
}
