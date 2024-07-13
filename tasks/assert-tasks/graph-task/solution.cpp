#include "bits/stdc++.h"
using namespace std;

vector<vector<int>> graph1;
vector<vector<int>> graph2;

int main() {
    int n, m;
    cin >> n >> m;
    graph1.resize(n);

    while(m--) {
        int a, b;
        cin >> a >> b;
        graph1[a].push_back(b);
    }

    int n2, m2;
    cin >> n2 >> m2;
    graph2.resize(n2);
    for(int i = 0; i < m2; i++) {
        int a, b;
        cin >> a >> b;
        graph2[a].push_back(b);
    }

    if (graph1 == graph2) {
        cout << "true";
    } else {
        cout << "false";
    }
}