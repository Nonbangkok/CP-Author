// Reference for lp_str02_wallpaper: the prefix function pi[L-1] is the longest
// proper border of the prefix of length L, and its shortest period is
// p = L - pi[L-1]. The prefix is c >= 2 copies of one block exactly when p
// divides L (then the smallest block has length p and c = L / p); otherwise
// the only "block" is the whole prefix, c = 1. O(N + Q).
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, q;
  string s;
  cin >> n >> q >> s;
  vector<int> pi(n, 0);
  for (int i = 1; i < n; i++) {
    int k = pi[i - 1];
    while (k > 0 && s[i] != s[k]) k = pi[k - 1];
    if (s[i] == s[k]) k++;
    pi[i] = k;
  }
  while (q--) {
    int len;
    cin >> len;
    int p = len - pi[len - 1];
    int copies = (len % p == 0) ? len / p : 1;
    cout << p << ' ' << copies << '\n';
  }
}
