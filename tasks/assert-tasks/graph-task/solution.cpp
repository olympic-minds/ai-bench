#include "testlib/graph.h"
#include "bits/stdc++.h"
using namespace std;

int compare_graphs(vector<vector<int>> graph1, vector<vector<int>> graph2) { return int(graph1 == graph2); }

int main() {
    Graph graph1 = Graph::read_graph(cin);
    Graph graph2 = Graph::read_graph(cin);

    cout << compare_graphs(graph1, graph2) << '\n';
}
