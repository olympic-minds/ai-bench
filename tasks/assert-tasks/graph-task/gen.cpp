#include "testlib/readwriter.h"
using namespace std;



void shortDifferentPaths(int testNumber) {

    // can't have 2 different paths of length 1 or 2
    int numOfNodes = rnd.next(3, 10); 
    Graph g1 = Graph::construct_path_graph(numOfNodes);
    Graph g2 = Graph::construct_path_graph(numOfNodes);
    while(g1 == g2) {
        g2 = Graph::construct_path_graph(numOfNodes);
    }

    string promptIn = g1.toString(Prompt) + g2.toString(Prompt); 
    string promptFilePath = dirs.at("promptInputDirectory") + "/" + std::to_string(testNumber) + ".in";
    printToFile(promptIn, promptFilePath);

    string solutionIn = g1.toString(Solution) + g2.toString(Solution); 
    string solutionFilePath = dirs.at("solutionInputDirectory") + "/" + std::to_string(testNumber) + ".in";
    printToFile(solutionIn, solutionFilePath);
}

int main(int argc, char *argv[]) {
    int seed;
    cin>>seed;
    registerGen(seed);
    setupDirectories();

    shortDifferentPaths(0);
}