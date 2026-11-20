// Naive O(NQ) scan: correct, and must time out on the last subtask.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, q;
  cin >> n >> q;
  vector<int> a(n);
  for (int &x : a) cin >> x;
  while (q--) {
    int l, r;
    cin >> l >> r;
    int count = 0;
    for (int x : a)
      if (l <= x && x <= r) count++;
    cout << count << '\n';
  }
}
