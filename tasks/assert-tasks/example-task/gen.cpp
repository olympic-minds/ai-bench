#include "testlib/readwriter.h"

using namespace std;

void printGraphToAppropriateFiles(int testNumber, const Graph& g);

void testEmptyGraph(int testNumber) {
    int numOfNodes = rnd.next(5, 10);
    printGraphToAppropriateFiles(testNumber, Graph::construct_undirected_clique(numOfNodes));
}

void testShortPath(int testNumber) {
    int numOfNodes = rnd.next(5, 10);
    printGraphToAppropriateFiles(testNumber, Graph::construct_path_graph(numOfNodes));
}

void testMultipleShortPaths(int testNumber) {
    int numOfNodes = rnd.next(8, 15);
    int numOfPaths = rnd.next(3, 6);
    printGraphToAppropriateFiles(testNumber, Graph::construct_path_graph(numOfNodes, numOfPaths));
}

void testSmallClique(int testNumber) {
    int numOfNodes = rnd.next(5, 10);

    printGraphToAppropriateFiles(testNumber, Graph::construct_undirected_clique(numOfNodes));
}

void testTree(int testNumber) {
    int numOfNodes = rnd.next(5, 10);

    printGraphToAppropriateFiles(testNumber, Graph::construct_tree_graph(numOfNodes));
}

void testForrest(int testNumber) {
    int numOfNodes = rnd.next(10, 15);
    int numberOfTrees = rnd.next(3, 4);
    printGraphToAppropriateFiles(testNumber, Graph::construct_forest_graph(numOfNodes, numberOfTrees));
}

void testShallowForrest(int testNumber) {
    int numOfNodes = rnd.next(10, 15);
    int numberOfTrees = rnd.next(3, 4);
    printGraphToAppropriateFiles(testNumber, Graph::construct_shallow_forest_graph(numOfNodes, numberOfTrees));
}

void testStarfish(int testNumber) {
    int numOfNodes = rnd.next(5, 20);
    int numOfRays = rnd.next(3, 4);
    int maxRayLength = 7;

    printGraphToAppropriateFiles(testNumber, Graph::construct_starfish_graph(numOfNodes, numOfRays, maxRayLength));
}

void testSparseGraph(int testNumber) {
    int numOfNodes = rnd.next(10, 15);
    printGraphToAppropriateFiles(testNumber, Graph::construct_sparse_graph(numOfNodes));
}

void testDenseGraph(int testNumber) {
    int numOfNodes = rnd.next(10, 15);
    printGraphToAppropriateFiles(testNumber, Graph::construct_dense_graph(numOfNodes));
}

int main() {
    int seed;
    cin >> seed;
    registerGen(seed);
    setupDirectories();

    std::map<int, std::function<void(int)>> tests = {{0, testEmptyGraph},
                                                     {1, testShortPath},
                                                     {2, testMultipleShortPaths},
                                                     {3, testSmallClique},
                                                     {4, testForrest},
                                                     {5, testShallowForrest},
                                                     // {6, testStarfish},
                                                     {7, testSparseGraph},
                                                     {8, testDenseGraph}};

    for (auto [testId, test] : tests) {
        test(testId);
    }
}
void printGraphToAppropriateFiles(int testNumber, const Graph& g) {
    auto [promptInStream, solutionInStream] = setupTest(testNumber);

    g.printTo(promptInStream, Prompt);
    g.printTo(solutionInStream, Solution);

    promptInStream.close();
    solutionInStream.close();
}
