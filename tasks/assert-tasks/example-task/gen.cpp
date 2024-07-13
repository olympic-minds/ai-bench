#include <bits/stdc++.h>
#include "testlib/testlib.h"

using namespace std;

int numberOfNodes, seed;
bool printForSolution;

string generate_graph();
int generate_int();

int maxEdges(int nodes) {
    assert(nodes >= 0);
    assert(nodes * (nodes - 1) / 2 >= 0);
    
    return nodes * (nodes - 1) / 2;
}

void printGraph(int numberOfNodes, set<pair<int,int>>& edges, bool forSolution) {
    if(forSolution) {
        cout << numberOfNodes << " " << edges.size() << "\n";
        for(auto edge: edges) {
            cout << edge.first << " " << edge.second << "\n";
        }
    } else { // for prompt
        cout << "{";
        vector<int> graph[numberOfNodes];
        for(auto edge: edges) {
            graph[edge.first].push_back(edge.second);
            graph[edge.second].push_back(edge.first);
        }       
        for (int i = 0; i < numberOfNodes; i++) {
            cout << "{";
            for (int j = 0; j < graph[i].size(); j++) {
                cout << graph[i][j];
                if (j != graph[i].size() - 1) {
                    cout << ",";
                }
            }
            cout << "}";
            if (i != numberOfNodes - 1) {
                cout << ",";
            }
        }
        cout << "}\n";
        cout << numberOfNodes << "\n";
    }
}


int main() {
    cin >> numberOfNodes >> seed >> printForSolution;
    registerGen(seed);
    assert(numberOfNodes > 0);
    int numberOfEdges = rnd.next(0, maxEdges(numberOfNodes));
    set<pair<int,int>> edges;
    while (edges.size() < numberOfEdges) {
        int from = rnd.next(0, numberOfNodes - 1);
        int to = rnd.next(0, numberOfNodes - 1);
        if (from > to) {
            swap(from, to);
        }
        if (from == to) continue;
        
        edges.insert({ from, to });
    }
    printGraph(numberOfNodes, edges, printForSolution);

    // cout << generate_graph(size, seed) << "\n" << generate_int(1, size, seed);
}
