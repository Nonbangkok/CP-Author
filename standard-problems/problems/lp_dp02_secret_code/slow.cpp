// Naive: enumerate every way to cut the string, one by one (depth-first with
// an explicit stack, so a long string cannot overflow the call stack), and
// count the ones that reach the end. The number of cuttings grows
// exponentially with N: correct, and must time out on the last subtask.
#include <bits/stdc++.h>
using namespace std;

const long long MOD = 1'000'000'007;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m;
  string s;
  cin >> n >> m >> s;
  long long count = 0;
  vector<int> stack = {0};  // positions where the next piece starts
  while (!stack.empty()) {
    int at = stack.back();
    stack.pop_back();
    if (at == n) {
      count = (count + 1) % MOD;
      continue;
    }
    if (s[at] == '0') continue;
    int value = 0;
    for (int len = 1; len <= 3 && at + len <= n; len++) {
      value = value * 10 + (s[at + len - 1] - '0');
      if (value <= m) stack.push_back(at + len);
    }
  }
  cout << count << '\n';
}
