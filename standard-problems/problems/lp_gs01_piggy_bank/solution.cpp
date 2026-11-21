// Reference for lp_gs01_piggy_bank: read until EOF into a long long sum.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  long long sum = 0, x;
  while (cin >> x) sum += x;
  cout << sum << '\n';
}
