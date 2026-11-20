// Naive O(N * K): keep the K best in a plain vector and scan it for the
// smallest one every day. Correct, and must time out on the last subtask.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, k;
  cin >> n >> k;
  vector<long long> best;
  long long sum = 0, total = 0;
  for (int i = 0; i < n; i++) {
    long long x;
    cin >> x;
    if ((int)best.size() < k) {
      best.push_back(x);
      sum += x;
    } else {
      size_t low = 0;
      for (size_t j = 1; j < best.size(); j++)
        if (best[j] < best[low]) low = j;
      if (x > best[low]) {
        sum += x - best[low];
        best[low] = x;
      }
    }
    total += sum;
  }
  cout << total << '\n';
}
