// Naive: a fresh BFS forwards from every query board until the solved board is
// reached. Correct, and fine for a single query, but up to 9! states per query
// is far too slow for hundreds of queries.
#include <bits/stdc++.h>
using namespace std;

const int BLOCK[4][4] = {{0, 1, 4, 3}, {1, 2, 5, 4}, {3, 4, 7, 6}, {4, 5, 8, 7}};
const int FACT[9] = {1, 1, 2, 6, 24, 120, 720, 5040, 40320};

int encode(const int *g) {
  int code = 0;
  for (int i = 0; i < 9; i++) code = code * 10 + g[i];
  return code;
}

void decode(int code, int *g) {
  for (int i = 8; i >= 0; i--) {
    g[i] = code % 10;
    code /= 10;
  }
}

int rankOf(const int *g) {
  int r = 0;
  for (int i = 0; i < 9; i++) {
    int smaller = 0;
    for (int j = i + 1; j < 9; j++) smaller += g[j] < g[i];
    r += smaller * FACT[8 - i];
  }
  return r;
}

int solve(int start) {
  vector<int> dist(362880, -1);
  vector<int> q;
  int g[9], h[9];
  decode(start, g);
  dist[rankOf(g)] = 0;
  q.push_back(start);
  for (size_t head = 0; head < q.size(); head++) {
    decode(q[head], g);
    int d = dist[rankOf(g)];
    if (q[head] == 123456789) return d;
    for (const auto &b : BLOCK) {
      memcpy(h, g, sizeof g);  // clockwise turn: each tile moves one step forward
      h[b[1]] = g[b[0]];
      h[b[2]] = g[b[1]];
      h[b[3]] = g[b[2]];
      h[b[0]] = g[b[3]];
      int r = rankOf(h);
      if (dist[r] != -1) continue;
      dist[r] = d + 1;
      q.push_back(encode(h));
    }
  }
  return -1;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int queries;
  cin >> queries;
  while (queries--) {
    int g[9];
    for (int &v : g) cin >> v;
    cout << solve(encode(g)) << '\n';
  }
}
