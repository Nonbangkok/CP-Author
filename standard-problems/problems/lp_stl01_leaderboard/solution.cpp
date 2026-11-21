// Reference for lp_stl01_leaderboard: one std::sort with a lambda comparator
// (score descending, then name ascending), O(N log N).
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<pair<string, int>> a(n);
  for (auto &[name, score] : a) cin >> name >> score;
  sort(a.begin(), a.end(), [](const pair<string, int> &x, const pair<string, int> &y) {
    if (x.second != y.second) return x.second > y.second;
    return x.first < y.first;
  });
  for (const auto &[name, score] : a) cout << name << ' ' << score << '\n';
}
