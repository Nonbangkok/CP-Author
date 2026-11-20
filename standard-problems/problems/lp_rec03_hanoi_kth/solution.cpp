// Reference for lp_rec03_hanoi_kth: move(n, x, y, z) is 2^(n-1) - 1 moves,
// then disk n, then 2^(n-1) - 1 moves, so the K-th move is found by
// descending into one half per level, O(N) per query.
#include <bits/stdc++.h>
using namespace std;

void kth(int n, int x, int y, int z, long long k) {
  long long half = 1LL << (n - 1);  // position of disk n's own move
  if (k == half) {
    cout << n << ' ' << x << ' ' << y << '\n';
  } else if (k < half) {
    kth(n - 1, x, z, y, k);
  } else {
    kth(n - 1, z, y, x, k - half);
  }
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, q;
  cin >> n >> q;
  while (q--) {
    long long k;
    cin >> k;
    kth(n, 1, 3, 2, k);
  }
}
