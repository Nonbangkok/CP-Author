// Reference for lp_mat02_patrol_routes: walks of length L from s to t are
// (A^L)[s][t], A[u][v] = number of corridors u -> v.
// Precompute P[i] = A^(2^i) once (60 squarings, O(60 N^3)), then each query
// multiplies the row vector e_s by P[i] for every set bit i of L: O(60 N^2)
// per query instead of a fresh O(N^3 log L) matrix power.
#include <bits/stdc++.h>
using namespace std;

const unsigned long long MOD = 1000000007ULL;
const int BITS = 60;  // 10^18 < 2^60
int n;
unsigned long long P[BITS][50][50];

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int m, q;
  cin >> n >> m >> q;
  for (int e = 0; e < m; e++) {
    int u, v;
    cin >> u >> v;
    P[0][u - 1][v - 1]++;
  }
  for (int b = 1; b < BITS; b++) {
    auto &x = P[b - 1];
    auto &z = P[b];
    for (int i = 0; i < n; i++)
      for (int k = 0; k < n; k++) {
        unsigned long long xik = x[i][k];
        if (xik == 0) continue;
        for (int j = 0; j < n; j++) z[i][j] = (z[i][j] + xik * x[k][j]) % MOD;
      }
  }
  vector<unsigned long long> vec(n), nxt(n);
  while (q--) {
    int s, t;
    long long len;
    cin >> s >> t >> len;
    fill(vec.begin(), vec.end(), 0);
    vec[s - 1] = 1;
    for (int b = 0; b < BITS; b++) {
      if (!((len >> b) & 1)) continue;
      fill(nxt.begin(), nxt.end(), 0);
      for (int k = 0; k < n; k++) {
        if (vec[k] == 0) continue;
        for (int j = 0; j < n; j++) nxt[j] = (nxt[j] + vec[k] * P[b][k][j]) % MOD;
      }
      swap(vec, nxt);
    }
    cout << vec[t - 1] << '\n';
  }
}
