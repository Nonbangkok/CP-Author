// Reference for lp_ss03_spin_tiles: one BFS from the solved board, run
// backwards (counter-clockwise turns undo clockwise ones), gives every board's
// distance to the goal; each query is then a lookup. Boards are numbered
// 0 .. 9!-1 by their Lehmer code, so the distances fit in a plain array.
#include <bits/stdc++.h>
using namespace std;

// the four 2x2 blocks, each listed clockwise: top-left, top-right, bottom-right, bottom-left
const int BLOCK[4][4] = {{0, 1, 4, 3}, {1, 2, 5, 4}, {3, 4, 7, 6}, {4, 5, 8, 7}};
const int FACT[9] = {1, 1, 2, 6, 24, 120, 720, 5040, 40320};

int encode(const int *g) {  // the 9 tiles row by row as one int, e.g. 123456789
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

int rankOf(const int *g) {  // position among all 9! orderings
  int r = 0;
  for (int i = 0; i < 9; i++) {
    int smaller = 0;
    for (int j = i + 1; j < 9; j++) smaller += g[j] < g[i];
    r += smaller * FACT[8 - i];
  }
  return r;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  vector<int> dist(362880, -1);
  vector<int> q;  // boards as 9-digit ints; q[head..] still to expand
  q.reserve(362880);
  int g[9], h[9];
  decode(123456789, g);
  dist[rankOf(g)] = 0;
  q.push_back(123456789);
  for (size_t head = 0; head < q.size(); head++) {
    decode(q[head], g);
    int d = dist[rankOf(g)];
    for (const auto &b : BLOCK) {
      // undo a clockwise turn = turn counter-clockwise: each tile moves one step back
      memcpy(h, g, sizeof g);
      h[b[0]] = g[b[1]];
      h[b[1]] = g[b[2]];
      h[b[2]] = g[b[3]];
      h[b[3]] = g[b[0]];
      int r = rankOf(h);
      if (dist[r] != -1) continue;
      dist[r] = d + 1;
      q.push_back(encode(h));
    }
  }
  int queries;
  cin >> queries;
  while (queries--) {
    for (int &v : g) cin >> v;
    cout << dist[rankOf(g)] << '\n';
  }
}
