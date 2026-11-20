// Naive: replay the whole recursion once, counting moves, and answer the
// queries (sorted) as their move numbers come up. O(max K): fine for N <= 20,
// hopeless for N = 60.
#include <bits/stdc++.h>
using namespace std;

long long counter = 0;
size_t nextQuery = 0;
vector<pair<long long, int>> queries;  // (K, original index)
vector<array<int, 3>> answer;

void play(int n, int x, int y, int z) {
  if (n == 0 || nextQuery == queries.size()) return;
  play(n - 1, x, z, y);
  counter++;
  while (nextQuery < queries.size() && queries[nextQuery].first == counter) {
    answer[queries[nextQuery].second] = {n, x, y};
    nextQuery++;
  }
  play(n - 1, z, y, x);
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, q;
  cin >> n >> q;
  queries.resize(q);
  answer.resize(q);
  for (int i = 0; i < q; i++) {
    cin >> queries[i].first;
    queries[i].second = i;
  }
  sort(queries.begin(), queries.end());
  play(n, 1, 3, 2);
  for (auto &a : answer) cout << a[0] << ' ' << a[1] << ' ' << a[2] << '\n';
}
