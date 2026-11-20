// Naive: for each query try p = 1, 2, ... and check s[i] == s[i + p] over the
// whole prefix (stopping at the first mismatch). O(L^2) per query on prefixes
// like "aaa...ab", where every p fails only at the very end.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, q;
  string s;
  cin >> n >> q >> s;
  while (q--) {
    int len;
    cin >> len;
    int p = 1;
    while (true) {
      bool ok = true;
      for (int i = 0; i + p < len; i++)
        if (s[i] != s[i + p]) {
          ok = false;
          break;
        }
      if (ok) break;
      p++;
    }
    int copies = (len % p == 0) ? len / p : 1;
    cout << p << ' ' << copies << '\n';
  }
}
