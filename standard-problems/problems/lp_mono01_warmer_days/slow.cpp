// Naive O(N^2): from every day, walk forward until a strictly warmer day.
// Correct, but a run of equal or falling temperatures makes every walk long:
// must time out on the last subtask.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> t(n);
  for (int &x : t) cin >> x;
  for (int i = 0; i < n; i++) {
    int d = 0;
    for (int j = i + 1; j < n; j++) {
      if (t[j] > t[i]) {
        d = j - i;
        break;
      }
    }
    cout << d << (i + 1 < n ? ' ' : '\n');
  }
}
