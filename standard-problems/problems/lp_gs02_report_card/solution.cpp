// Reference for lp_gs02_report_card: integer sums, divide as double at the
// end, print with fixed << setprecision(2).
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m;
  cin >> n >> m;
  long long total = 0;
  cout << fixed << setprecision(2);
  for (int i = 0; i < n; i++) {
    long long sum = 0;
    for (int j = 0; j < m; j++) {
      int x;
      cin >> x;
      sum += x;
    }
    total += sum;
    cout << (double)sum / m << '\n';
  }
  cout << (double)total / ((long long)n * m) << '\n';
}
