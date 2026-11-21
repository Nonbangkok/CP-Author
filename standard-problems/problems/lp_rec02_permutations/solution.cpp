// Reference for lp_rec02_permutations: backtracking over letter counts.
// Trying the letters 'a'..'z' in order at every position yields the distinct
// permutations already in lexicographic order, each exactly once.
#include <bits/stdc++.h>
using namespace std;

int n;
int cnt[26];
string cur;
string out;

void gen() {
  if ((int)cur.size() == n) {
    out += cur;
    out += '\n';
    return;
  }
  for (int c = 0; c < 26; c++) {
    if (cnt[c] == 0) continue;
    cnt[c]--;
    cur.push_back(char('a' + c));
    gen();
    cur.pop_back();
    cnt[c]++;
  }
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string w;
  cin >> w;
  n = w.size();
  for (char ch : w) cnt[ch - 'a']++;
  gen();
  cout << out;
}
