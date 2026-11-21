// Naive: try S = max(a), max(a) + 1, ... until the greedy check passes.
// Correct, but the answer can be ~10^13 above max(a): times out on the last subtask.
#include <bits/stdc++.h>
using namespace std;

int n, k;
vector<long long> a;

bool ok(long long cap) {
  int parts = 1;
  long long current = 0;
  for (long long v : a) {
    if (v > cap) return false;
    if (current + v > cap) {
      parts++;
      current = 0;
    }
    current += v;
  }
  return parts <= k;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  cin >> n >> k;
  a.resize(n);
  for (long long &v : a) cin >> v;
  long long cap = *max_element(a.begin(), a.end());
  while (!ok(cap)) cap++;
  cout << cap << '\n';
}
