// Naive O(N * K): keep the strips found so far unsorted; each new interval
// scans all of them and swallows the ones it touches. Correct, and must time
// out on the last subtask.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<pair<long long, long long>> strips;
  for (int i = 0; i < n; i++) {
    long long l, r;
    cin >> l >> r;
    for (size_t j = 0; j < strips.size();) {
      if (strips[j].first <= r && l <= strips[j].second) {
        l = min(l, strips[j].first);
        r = max(r, strips[j].second);
        strips[j] = strips.back();
        strips.pop_back();
      } else {
        j++;
      }
    }
    strips.push_back({l, r});
  }
  long long total = 0;
  for (auto &[l, r] : strips) total += r - l;
  cout << strips.size() << '\n' << total << '\n';
}
