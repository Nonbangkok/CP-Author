// Naive O(N Q): walk from bay l to the right until a tall enough ceiling or
// bay r. Correct, and must time out on the last subtask.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, q;
  cin >> n >> q;
  vector<int> h(n + 1);
  for (int i = 1; i <= n; i++) cin >> h[i];
  while (q--) {
    int type;
    cin >> type;
    if (type == 1) {
      int i, y;
      cin >> i >> y;
      h[i] = y;
    } else {
      int l, r, x;
      cin >> l >> r >> x;
      int found = -1;
      for (int j = l; j <= r; j++) {
        if (h[j] >= x) { found = j; break; }
      }
      cout << found << '\n';
    }
  }
}
