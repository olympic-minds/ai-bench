#include<bits/stdc++.h>
using namespace std;

vector<vector<int>> graph;

vector<int> ans;
bool visited[1000000];

void dfs (int v) {
    ans.push_back(v);
    visited[v] = true;
    for (int u : graph[v]) {
        if (!visited[u]) {
            dfs(u);
        }
    }
}

vector<int> DFS(int v) {
    dfs(v);
    return ans;
}

int main () {
    int n, m;
    cin >> n >> m;
    graph.resize(n);
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        graph[u].push_back(v);
        graph[v].push_back(u);
    }

    vector<int> res = DFS(0);
    cout << "{";
    for (int i = 0 ; i < res.size() ; i++) {
        cout << res[i]; 
        if (i != res.size() - 1) {
            cout << ",";
        }
    }
    cout << "}";

    return 0;
}
