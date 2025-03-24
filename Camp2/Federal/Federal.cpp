#include <bits/stdc++.h>
#define coutf(n, m) cout << fixed << setprecision(n) << m
#define forr(i, a, n) for (int i = a; i < n; i++)
#define forl(i, a, n) for (int i = a; i > n; i--)
#define macos ios::sync_with_stdio(0);cin.tie(0);cout.tie(0)
#define endll "\n"
#define sp " "
typedef long long ll;
using namespace std;

struct Non{
    int v,time;

    bool operator < (const Non &rhs)const{
        if(time!=rhs.time)return time>rhs.time;
        return v>rhs.v;
    }
};

const int N = 2010;
int t[N],indeg[N],end_time[N];
int n,m,w,a,b,t2,finish,ans;
vector<int> adj[N];
priority_queue<Non> q;
priority_queue<int,vector<int>,greater<int>> work;

int main(){macos;

    cin >> n >> m >> w;
    forr(i,0,n)cin >> t[i];
    forr(i,0,m){
        cin >> a >> b;
        adj[a].push_back(b);
        indeg[b]++;
    }

    forr(i,0,n)if(!indeg[i])q.push({i,0});
    forr(i,0,w)work.push(0);

    while(!q.empty()){
        auto [u,t1] = q.top();
        q.pop();

        t2 = work.top();
        work.pop();

        finish = max(t1,t2) + t[u];
        ans = max(ans,finish);

        work.push(finish);

        for(auto v:adj[u]){
            indeg[v]--;
            end_time[v] = max(end_time[v],finish);
            if(!indeg[v])q.push({v,end_time[v]});
        }
    }

    cout << ans;

    return 0;
}