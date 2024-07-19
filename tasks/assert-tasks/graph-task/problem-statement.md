```cpp
#include<bits/stdc++.h>
using namespace std;

vector<vector<int>> graph1 = @IN_1;
vector<vector<int>> graph2 = @IN_2;

int compare_graphs(vector<vector<int>> graph1, vector<vector<int>> graph2) {
	return int(graph1 == graph2);
}

assert(compare_graphs({{1}, {0}}, {{1}, {0}}) == 1);
assert(compare_graphs({{}, {2}, {1}}}, {{1}, {0}, {}}) == 0);
assert(compare_graphs(@IN_1, @IN_2) == @ANS);
```
