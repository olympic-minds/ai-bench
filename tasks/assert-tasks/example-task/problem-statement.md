Make sure you use a valid c++ vector definition. Only output the values in brackets
```cpp
#include<bits/stdc++.h>
using namespace std;

vector<int> graph[] = @IN_1

vector<int> ans;
bool visited[@IN_2];

vector<int> DFS(int v) {
    dfs(v);
    return ans;
}

void dfs (int v) {
    ans.push_back(v);
    visited[v] = true;
    for (int u : graph[v]) {
        if (!visited[u]) {
            dfs(u);
        }
    }
}

assert(DFS(0) == vector<int>(@ANS));
```
