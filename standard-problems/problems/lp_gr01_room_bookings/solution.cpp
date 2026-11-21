// Reference for lp_gr01_room_bookings: activity selection.
// Booking i blocks the half-open interval [s_i, s_i + d_i + C): the room is in
// use, then cleaned. Sort by end and take every booking that starts no earlier
// than the previous accepted end + C. O(N log N).
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  long long c;
  cin >> n >> c;
  vector<pair<long long, long long>> b(n);  // (end, start)
  for (auto &[e, s] : b) {
    long long d;
    cin >> s >> d;
    e = s + d;
  }
  sort(b.begin(), b.end());
  int taken = 0;
  long long freeAt = LLONG_MIN;  // earliest start allowed for the next booking
  for (auto &[e, s] : b) {
    if (s >= freeAt) {
      taken++;
      freeAt = e + c;
    }
  }
  cout << taken << '\n';
}
