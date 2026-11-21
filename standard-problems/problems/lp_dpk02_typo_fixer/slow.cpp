// Naive: the same recurrence by plain recursion, no memo. cost(i, j) calls
// itself three times, so the number of calls is a Delannoy number that grows
// exponentially: correct, and must time out on the last subtask.
// Depth <= |A| + |B|.
#include <bits/stdc++.h>
using namespace std;

string a, b;
int ins, del, rep;

int cost(int i, int j) {  // turn A[0..i) into B[0..j)
  if (i == 0) return j * ins;
  if (j == 0) return i * del;
  int keep = cost(i - 1, j - 1) + (a[i - 1] == b[j - 1] ? 0 : rep);
  return min({cost(i - 1, j) + del, cost(i, j - 1) + ins, keep});
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  cin >> a >> b >> ins >> del >> rep;
  cout << cost(a.size(), b.size()) << '\n';
}
