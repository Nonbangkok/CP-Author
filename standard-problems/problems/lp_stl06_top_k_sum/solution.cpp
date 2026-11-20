// Reference for lp_stl06_top_k_sum: a min-heap holds the K largest scores, its
// top is the weakest of them; keep their sum as we go, O(N log K).
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, k;
  cin >> n >> k;
  priority_queue<long long, vector<long long>, greater<long long>> best;
  long long sum = 0, total = 0;
  for (int i = 0; i < n; i++) {
    long long x;
    cin >> x;
    best.push(x);
    sum += x;
    if ((int)best.size() > k) {
      sum -= best.top();
      best.pop();
    }
    total += sum;
  }
  cout << total << '\n';
}
