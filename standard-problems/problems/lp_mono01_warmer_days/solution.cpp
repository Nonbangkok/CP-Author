// Reference for lp_mono01_warmer_days: monotonic stack, O(N).
// The stack keeps the indices of days still waiting for a warmer day; their
// temperatures are non-increasing from bottom to top. A new day pops (and
// answers) every waiting day that is strictly colder. Each index is pushed and
// popped at most once.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<int> t(n);
  for (int &x : t) cin >> x;
  vector<int> d(n, 0);
  vector<int> st;
  for (int i = 0; i < n; i++) {
    while (!st.empty() && t[st.back()] < t[i]) {
      d[st.back()] = i - st.back();
      st.pop_back();
    }
    st.push_back(i);
  }
  for (int i = 0; i < n; i++) cout << d[i] << (i + 1 < n ? ' ' : '\n');
}
