```cpp
int hash_vector(const vector<int> &vec) {
    int result = 0;
    for (int i = 0; i < (int)vec.size(); i++) {
        result += (i + 1) * vec[i];
    }
    return result;
}

vector<vector<int>> graph;

vector<int> ans;
vector<bool> visited;

void dfs(int v) {
    ans.push_back(v);
    visited[v] = true;
    for (int u : graph[v]) {
        if (!visited[u]) {
            dfs(u);
        }
    }
}

int DFS(vector<vector<int>> g) {
    graph = g;
    visited.assign(graph.size(), false);
    dfs(0);
    return hash_vector(ans);
}

assert(DFS({{0}, {1}}) == 2);
assert(DFS(@IN_1) == @ANS);
```
