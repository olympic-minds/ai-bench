#include "testlib/readwriter.h"
using namespace std;

void printGraphsToAppropriateFiles(int testNumber, const Graph& g1, const Graph& g2);

std::pair<Graph, Graph> differentPaths(int testNumber, int length) {
    // can't have 2 different paths of length 1 or 2
    assert(length >= 3);
    Graph g1 = Graph::construct_path_graph(length);
    Graph g2 = Graph::construct_path_graph(length);
    while(g1 == g2) {
        g2 = Graph::construct_path_graph(length);
    }
    return {g1, g2};
}

std::pair<Graph, Graph> equalPaths(int testNumber, int length) {
    Graph g1 = Graph::construct_path_graph(length);
    return {g1, g1};
}

void shortDifferentPaths(int testNumber) {
    int numOfNodes = rnd.next(3, 10); 
    auto [g1, g2] = differentPaths(testNumber, numOfNodes);

    printGraphsToAppropriateFiles(testNumber, g1, g2);
}

void longDifferentPaths(int testNumber) {

    int numOfNodes = rnd.next(30, 100); 
    auto [g1, g2] = differentPaths(testNumber, numOfNodes);

    printGraphsToAppropriateFiles(testNumber, g1, g2);
}

void shortEqualPaths(int testNumber) {
    int numOfNodes = rnd.next(3, 10); 
    auto [g1, g2] = equalPaths(testNumber, numOfNodes);

    printGraphsToAppropriateFiles(testNumber, g1, g2);
}

void smallEqualCliques(int testNumber) {
    int numOfNodes = rnd.next(3, 10); 
    Graph g1 = Graph::construct_undirected_clique(numOfNodes);

    printGraphsToAppropriateFiles(testNumber, g1, g1);
}

// generate different size cliques
void smallDifferentCliques(int testNumber) {
    int numOfNodes1 = rnd.next(3, 10); 
    Graph g1 = Graph::construct_undirected_clique(numOfNodes1);
    int numOfNodes2 = rnd.next(numOfNodes1, std::max(10, numOfNodes1 + 1)); 
    Graph g2 = Graph::construct_undirected_clique(numOfNodes2);

    printGraphsToAppropriateFiles(testNumber, g1, g2);
}

void smallEqualTreeOfDegree2to4(int testNumber) {
    int numOfNodes = rnd.next(5, 20); 
    Graph g1 = Graph::construct_tree_of_bounded_degree_graph(numOfNodes, 2, 4);

    printGraphsToAppropriateFiles(testNumber, g1, g1);
}

void smallDifferentTreeOfDegree2to4(int testNumber) {
    int numOfNodes = rnd.next(5, 20); 
    int minDegree = 2, maxDegree = 4;
    Graph g1 = Graph::construct_tree_of_bounded_degree_graph(numOfNodes, minDegree, maxDegree);
    Graph g2 = Graph::construct_tree_of_bounded_degree_graph(numOfNodes, minDegree, maxDegree);
    while (g1 == g2) {
        g2 = Graph::construct_tree_of_bounded_degree_graph(numOfNodes, minDegree, maxDegree);
    }

    printGraphsToAppropriateFiles(testNumber, g1, g2);
}

void smallDifferentForrests(int testNumber) {
    int numOfNodes = rnd.next(5, 20); 
    int numOfTrees = rnd.next(3, min(5, numNodes - 1));
    Graph g1 = Graph::construct_forest_graph(numOfNodes, numOfTrees);
    Graph g2 = Graph::construct_forest_graph(numOfNodes, numOfTrees);
    while (g1 == g2) {
        g2 = Graph::construct_forest_graph(numOfNodes, numOfTrees);
    }

    printGraphsToAppropriateFiles(testNumber, g1, g2);
}

void smallEqualForrests(int testNumber) {
    int numOfNodes = rnd.next(5, 20); 
    int numOfTrees = rnd.next(3, 5);
    Graph g1 = Graph::construct_forest_graph(numOfNodes, numOfTrees);
    printGraphsToAppropriateFiles(testNumber, g1, g1);
}

void smallDifferentStarfishes(int testNumber) {
    int numOfNodes = rnd.next(5, 20); 
    int numOfRays = rnd.next(3, 4);
    int maxRayLength = 7; 
    Graph g1 = Graph::construct_starfish_graph(numOfNodes, maxRayLength, numOfRays);
    Graph g2 = Graph::construct_starfish_graph(numOfNodes, maxRayLength, numOfRays);
    while (g1 == g2) {
        g2 = Graph::construct_starfish_graph(numOfNodes, maxRayLength, numOfRays);
    }

    printGraphsToAppropriateFiles(testNumber, g1, g2);
}

void smallEqualStarfishes(int testNumber) {
    int numOfNodes = rnd.next(5, 20); 
    int numOfRays = rnd.next(3, 4);
    int maxRayLength = 7; 
    Graph g = Graph::construct_starfish_graph(numOfNodes, maxRayLength, numOfRays);

    printGraphsToAppropriateFiles(testNumber, g, g);
}

int main(int argc, char *argv[]) {
    int seed;
    cin>>seed;
    registerGen(seed);
    setupDirectories();

    std::map<int, std::function<void(int)>> tests = {
        {0, shortDifferentPaths},
        {1, shortEqualPaths},
        {2, smallDifferentCliques},
        {3, smallEqualCliques},
        {4, smallDifferentTreeOfDegree2to4},
        {5, smallEqualTreeOfDegree2to4},
        {6, smallDifferentForrests},
        {7, smallEqualForrests},
        // {8, smallDifferentStarfishes},
        // {9, smallEqualStarfishes}
    };

    for(auto [testId, test]: tests) {
        test(testId);
    }
}

void printGraphsToAppropriateFiles(int testNumber, const Graph& g1, const Graph& g2) {
    string promptIn = g1.toString(Prompt) + g2.toString(Prompt); 
    string promptFilePath = dirs.at("promptInputDirectory") + "/" + std::to_string(testNumber) + ".in";
    printToFile(promptIn, promptFilePath);

    string solutionIn = g1.toString(Solution) + g2.toString(Solution); 
    string solutionFilePath = dirs.at("solutionInputDirectory") + "/" + std::to_string(testNumber) + ".in";
    printToFile(solutionIn, solutionFilePath);
}
