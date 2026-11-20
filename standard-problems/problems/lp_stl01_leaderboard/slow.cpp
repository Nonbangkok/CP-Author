// Naive bubble sort, O(N^2): correct, and must time out on the last subtask.
#include <bits/stdc++.h>
using namespace std;

bool before(const pair<string, int> &x, const pair<string, int> &y) {
  if (x.second != y.second) return x.second > y.second;
  return x.first < y.first;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<pair<string, int>> a(n);
  for (auto &[name, score] : a) cin >> name >> score;
  for (int i = 0; i < n; i++)
    for (int j = 0; j + 1 < n - i; j++)
      if (before(a[j + 1], a[j])) swap(a[j], a[j + 1]);
  for (const auto &[name, score] : a) cout << name << ' ' << score << '\n';
}
