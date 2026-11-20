// Reference for lp_swp03_low_awning: offline sweep with a multiset of the
// heights of the awnings that are "open", O((N + Q) log (N + Q)).
// Events sorted by position; at equal positions: open (0) < query (1) < close (2),
// because both ends are inclusive.
#include <bits/stdc++.h>
using namespace std;

struct Event {
  long long x;
  int kind;   // 0 = open, 1 = query, 2 = close
  long long value;  // height for open/close, query index for query
};

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, q;
  cin >> n >> q;
  vector<Event> ev;
  ev.reserve(2 * n + q);
  for (int i = 0; i < n; i++) {
    long long l, r, h;
    cin >> l >> r >> h;
    ev.push_back({l, 0, h});
    ev.push_back({r, 2, h});
  }
  for (int j = 0; j < q; j++) {
    long long p;
    cin >> p;
    ev.push_back({p, 1, j});
  }
  sort(ev.begin(), ev.end(), [](const Event &a, const Event &b) {
    if (a.x != b.x) return a.x < b.x;
    return a.kind < b.kind;
  });
  multiset<long long> open;
  vector<long long> answer(q);
  for (const Event &e : ev) {
    if (e.kind == 0) {
      open.insert(e.value);
    } else if (e.kind == 2) {
      open.erase(open.find(e.value));  // erase ONE copy, not every equal height
    } else {
      answer[e.value] = open.empty() ? -1 : *open.begin();
    }
  }
  for (int j = 0; j < q; j++) cout << answer[j] << '\n';
}
