// Reference for lp_bit03_light_switches: pressing a switch twice cancels
// (x ^ t ^ t = x) and the order of presses does not matter, so every answer is
// a SET of switches. Enumerate all 2^M sets; xr[set] = xr[set without its
// lowest bit] ^ t[lowest bit], and keep the smallest popcount that reaches
// target = (lamps that are off now). O(2^M).
#include <bits/stdc++.h>
using namespace std;

long long readMask(const string &s) {
  long long mask = 0;
  for (size_t p = 0; p < s.size(); p++)
    if (s[p] == '1') mask |= 1LL << p;
  return mask;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m;
  cin >> n >> m;
  string s;
  cin >> s;
  long long all = (1LL << n) - 1;
  long long target = readMask(s) ^ all;
  vector<long long> t(m);
  for (int j = 0; j < m; j++) {
    string row;
    cin >> row;
    t[j] = readMask(row);
  }
  int total = 1 << m;
  vector<long long> xr(total, 0);
  int best = target == 0 ? 0 : -1;
  for (int set = 1; set < total; set++) {
    xr[set] = xr[set & (set - 1)] ^ t[__builtin_ctz(set)];
    if (xr[set] == target) {
      int presses = __builtin_popcount(set);
      if (best == -1 || presses < best) best = presses;
    }
  }
  cout << best << '\n';
}
