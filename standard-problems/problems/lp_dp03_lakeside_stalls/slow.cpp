// Naive: try every valid choice of spots (no two neighbours on the circle),
// depth-first with an explicit stack, and keep the best total. The number of
// valid choices grows like 1.618^N: correct, and must time out on the last
// subtask.
#include <bits/stdc++.h>
using namespace std;

struct State {
  int i;          // next spot to decide
  long long sum;  // profit so far
  bool first;     // spot 0 is used
  bool prev;      // spot i - 1 is used
};

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<long long> a(n);
  for (long long &x : a) cin >> x;
  long long best = 0;
  vector<State> stack = {{1, a[0], true, true}, {1, 0, false, false}};
  while (!stack.empty()) {
    State s = stack.back();
    stack.pop_back();
    if (s.i == n) {
      best = max(best, s.sum);
      continue;
    }
    stack.push_back({s.i + 1, s.sum, s.first, false});                // leave spot i empty
    bool blocked = s.prev || (s.i == n - 1 && s.first);
    if (!blocked) stack.push_back({s.i + 1, s.sum + a[s.i], s.first, true});
  }
  cout << best << '\n';
}
