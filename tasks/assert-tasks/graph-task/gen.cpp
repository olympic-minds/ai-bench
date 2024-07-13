#include "testlib/readwriter.h"
using namespace std;


int main(int argc, char *argv[]) {
    int n, seed, format;
    cin>>n>>seed>>format;
    registerGen(seed);
    Graph g1 = Graph::construct_path_graph(n);
    g1.print(format);
    Graph g2 = Graph::construct_path_graph(n);
    g2.print(format);
}