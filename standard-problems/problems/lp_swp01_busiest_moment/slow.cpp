// Naive O(N^2): the busiest moment is always some arrival time, so for every
// guest count who is present at a_i. Correct, must time out on the last subtask.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<long long> a(n), b(n);
  for (int i = 0; i < n; i++) cin >> a[i] >> b[i];
  int best = 0;
  long long when = 0;
  for (int i = 0; i < n; i++) {
    int here = 0;
    for (int j = 0; j < n; j++)
      if (a[j] <= a[i] && a[i] < b[j]) here++;
    if (here > best || (here == best && a[i] < when)) {
      best = here;
      when = a[i];
    }
  }
  cout << best << ' ' << when << '\n';
}
