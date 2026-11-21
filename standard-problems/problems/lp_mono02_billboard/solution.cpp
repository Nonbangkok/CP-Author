// Reference for lp_mono02_billboard: largest rectangle in a histogram with
// widths, one monotonic stack, O(N). The best rectangle is as tall as the
// lowest building it covers, so try every building i as that lowest one: it
// stretches from just after the previous strictly lower building to just
// before the next lower-or-equal one (ties are fine: the last of the equal
// buildings gets the full stretch). x[i] = total width of buildings 0..i-1.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<long long> w(n), h(n), x(n + 1, 0);
  for (int i = 0; i < n; i++) {
    cin >> w[i] >> h[i];
    x[i + 1] = x[i] + w[i];
  }
  long long best = 0;
  vector<int> st;  // indices, heights strictly increasing from bottom to top
  for (int i = 0; i <= n; i++) {
    long long cur = (i == n) ? 0 : h[i];  // a height-0 sentinel flushes the stack
    while (!st.empty() && h[st.back()] >= cur) {
      int top = st.back();
      st.pop_back();
      long long left = st.empty() ? 0 : x[st.back() + 1];
      best = max(best, h[top] * (x[i] - left));
    }
    st.push_back(i);
  }
  cout << best << '\n';
}
