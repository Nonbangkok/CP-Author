// Reference for lp_str03_common_prefix: polynomial hashing mod 2^61 - 1 with a
// random base, so any substring's hash comes from two prefix hashes in O(1);
// "the first m letters match" is true ... true false ... false in m, so binary
// search the longest common prefix. O(N + Q log N).
#include <bits/stdc++.h>
using namespace std;

typedef unsigned long long ull;
const ull MOD = (1ULL << 61) - 1;

ull mulmod(ull a, ull b) {
  unsigned __int128 p = (unsigned __int128)a * b;
  ull lo = (ull)(p & MOD), hi = (ull)(p >> 61);
  ull r = lo + hi;  // 2^61 = 1 (mod 2^61 - 1)
  return r >= MOD ? r - MOD : r;
}

int n, q;
string s;
vector<ull> h, pw;

ull sub(int start, int len) {  // hash of s[start .. start+len)
  ull x = h[start + len] + MOD - mulmod(h[start], pw[len]);
  return x >= MOD ? x - MOD : x;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  cin >> n >> q >> s;
  mt19937_64 rng(chrono::steady_clock::now().time_since_epoch().count());
  ull base = rng() % (MOD - 1000) + 500;
  h.assign(n + 1, 0);
  pw.assign(n + 1, 1);
  for (int i = 0; i < n; i++) {
    h[i + 1] = mulmod(h[i], base) + (ull)s[i];
    if (h[i + 1] >= MOD) h[i + 1] -= MOD;
    pw[i + 1] = mulmod(pw[i], base);
  }
  while (q--) {
    int a, b;
    cin >> a >> b;
    a--, b--;
    int lo = 0, hi = n - max(a, b);  // the first lo letters match; the answer is <= hi
    while (lo < hi) {
      int m = (lo + hi + 1) / 2;
      if (sub(a, m) == sub(b, m)) lo = m;
      else hi = m - 1;
    }
    cout << lo << '\n';
  }
}
