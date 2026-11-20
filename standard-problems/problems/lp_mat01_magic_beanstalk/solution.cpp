// Reference for lp_mat01_magic_beanstalk: matrix exponentiation.
// State (f_n, f_{n-1}, 1); one step is the 3x3 matrix
//   [a b c]
//   [1 0 0]
//   [0 0 1]
// so (f_N, f_{N-1}, 1) = M^(N-1) (f_1, f_0, 1) for N >= 1. O(27 log N).
#include <bits/stdc++.h>
using namespace std;

const long long MOD = 1000000007LL;
using Matrix = array<array<long long, 3>, 3>;

Matrix multiply(const Matrix &x, const Matrix &y) {
  Matrix z{};
  for (int i = 0; i < 3; i++)
    for (int k = 0; k < 3; k++)
      for (int j = 0; j < 3; j++) z[i][j] = (z[i][j] + x[i][k] * y[k][j]) % MOD;
  return z;
}

int main() {
  long long a, b, c, f0, f1, n;
  cin >> a >> b >> c >> f0 >> f1 >> n;
  if (n == 0) {
    cout << f0 % MOD << '\n';
    return 0;
  }
  Matrix m{};
  m[0] = {a % MOD, b % MOD, c % MOD};
  m[1] = {1, 0, 0};
  m[2] = {0, 0, 1};
  Matrix r{};
  for (int i = 0; i < 3; i++) r[i][i] = 1;
  long long e = n - 1;
  while (e > 0) {
    if (e & 1) r = multiply(r, m);
    m = multiply(m, m);
    e >>= 1;
  }
  long long answer = (r[0][0] * (f1 % MOD) + r[0][1] * (f0 % MOD) % MOD + r[0][2]) % MOD;
  cout << answer << '\n';
}
