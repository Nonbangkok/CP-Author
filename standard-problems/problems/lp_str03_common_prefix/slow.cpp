// Naive: compare letter by letter until the first mismatch. O(answer) per
// query, so O(N * Q) on strings like "aaaa...a".
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, q;
  string s;
  cin >> n >> q >> s;
  while (q--) {
    int a, b;
    cin >> a >> b;
    a--, b--;
    int k = 0;
    while (a + k < n && b + k < n && s[a + k] == s[b + k]) k++;
    cout << k << '\n';
  }
}
