// Reference for lp_swp01_busiest_moment: sweep over +1/-1 events, O(N log N).
// A guest is present on [a, b), so at equal times the leave (-1) must come
// before the arrival (+1). Each event is packed into one number 2*time + kind
// (kind 0 = leave, 1 = arrive), so a plain sort gives exactly that order.
// The count right after a +1 event is the count at that time; the first time
// the maximum is reached is the answer's moment.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<long long> ev;
  ev.reserve(2 * n);
  for (int i = 0; i < n; i++) {
    long long a, b;
    cin >> a >> b;
    ev.push_back(2 * a + 1);
    ev.push_back(2 * b);
  }
  sort(ev.begin(), ev.end());
  int cur = 0, best = 0;
  long long when = 0;
  for (long long e : ev) {
    cur += (e & 1) ? +1 : -1;
    if (cur > best) {
      best = cur;
      when = e / 2;
    }
  }
  cout << best << ' ' << when << '\n';
}
