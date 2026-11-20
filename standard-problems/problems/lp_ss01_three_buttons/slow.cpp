// Naive: iterative deepening DFS with no visited set -- try every sequence of
// presses of length 0, 1, 2, ... Correct, but 3^answer sequences: fine while the
// answer is at most 12, hopeless when it is above 20.
#include <bits/stdc++.h>
using namespace std;

int L, S, T;

int reverseDigits(int x) {
  int r = 0;
  while (x > 0) {
    r = r * 10 + x % 10;
    x /= 10;
  }
  return r;
}

bool dfs(long long x, int left) {
  if (x == T) return true;
  if (left == 0) return false;
  long long nexts[3] = {2 * x, x - 1, (long long)reverseDigits((int)x)};
  for (long long y : nexts)
    if (y >= 1 && y <= L && dfs(y, left - 1)) return true;
  return false;
}

int main() {
  cin >> L >> S >> T;
  int depth = 0;
  while (!dfs(S, depth)) depth++;
  cout << depth << '\n';
}
