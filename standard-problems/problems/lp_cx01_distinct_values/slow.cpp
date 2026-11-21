// Naive O(N^2): a value is new when no earlier element equals it. Correct,
// and must time out on the last subtask.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> a(n);
  for (int &x : a) cin >> x;
  int distinct = 0;
  for (int i = 0; i < n; i++) {
    bool seen = false;
    for (int j = 0; j < i; j++)
      if (a[j] == a[i]) {
        seen = true;
        break;
      }
    if (!seen) distinct++;
  }
  cout << distinct << '\n';
}
