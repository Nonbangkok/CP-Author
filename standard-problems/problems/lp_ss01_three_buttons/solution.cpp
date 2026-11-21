// Reference for lp_ss01_three_buttons: BFS over the states 1..L.
// Every press costs 1, so the first time BFS reaches T is the minimum. O(L * digits).
#include <bits/stdc++.h>
using namespace std;

int reverseDigits(int x) {
  int r = 0;
  while (x > 0) {
    r = r * 10 + x % 10;
    x /= 10;
  }
  return r;
}

int main() {
  int L, S, T;
  cin >> L >> S >> T;
  vector<int> dist(L + 1, -1);
  queue<int> q;
  dist[S] = 0;
  q.push(S);
  while (!q.empty()) {
    int x = q.front();
    q.pop();
    if (x == T) break;
    long long nexts[3] = {2LL * x, x - 1LL, (long long)reverseDigits(x)};
    for (long long y : nexts) {
      if (y < 1 || y > L || dist[y] != -1) continue;
      dist[y] = dist[x] + 1;
      q.push((int)y);
    }
  }
  cout << dist[T] << '\n';
}
