// Naive O(N * D): a vector of (word, count) searched linearly every time.
// Correct, and must time out on the last subtask.
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n;
  cin >> n;
  vector<pair<string, int>> seen;
  string w;
  for (int i = 0; i < n; i++) {
    cin >> w;
    size_t j = 0;
    while (j < seen.size() && seen[j].first != w) j++;
    if (j == seen.size()) seen.push_back({w, 0});
    cout << ++seen[j].second << '\n';
  }
}
