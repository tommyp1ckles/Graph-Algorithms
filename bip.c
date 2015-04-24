/*
 * File:        bip.c
 * Author:      Tom Hadlaw
 * Date:        07/03/2015
 * Version:     1.0
 * Purpose:     Reads graph from stdin and checks if graph is bipartite,
 *              printing partitions if graph is bipartite and printing (an) odd
 *              cycle in the graph otherwise.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Vertex {
    int label;
    int seen;
    int seen2;
    int parity;
    int color;
    int vertexNum;
    int degree;
    char visited;
    struct Vertex** adj;
} vertex;

typedef struct Graph {
    int n;
    int maxDegree;
    vertex *V;
} Graph;

/*
 * Name:        initGraph
 * Purpose:     Initializes Graph struct.
 */
void initGraph(Graph *G, int n) {
    G->n = n;
    G->V = (vertex*) malloc(sizeof(vertex) * n);
    G->maxDegree = 0;
    int i;
    for (i = 0; i < n; i++) {
        G->V[i].label = 0;
        G->V[i].vertexNum = i;
        G->V[i].adj = malloc(sizeof(vertex*) * n);
        G->V[i].degree = 0;
        G->V[i].visited = 0;
        G->V[i].color = -1;
        G->V[i].parity = -1;
        G->V[i].seen = 0;
        G->V[i].seen2 = 0;
    }
}

/*
 * Name:        addEdge
 * Purpose:     Adds edge ViVj to graph G.
 * Arguments:   Pointer to Graph, first index of edge and second index of edge.
 */
void addEdge(Graph *G, int i, int j) {
    G->V[i].adj[G->V[i].degree] = &G->V[j];
    G->V[i].degree++;
    G->V[j].adj[G->V[j].degree] = &G->V[i];
    G->V[j].degree++;
    if (G->V[i].degree > G->maxDegree)
        G->maxDegree = G->V[i].degree;
    if (G->V[j].degree > G->maxDegree)
        G->maxDegree = G->V[j].degree;
}

/*
 * Name:        readGraphStdin
 * Purpose:     Reads graph date from stdin and creates graph from data.
 * Returns:     Pointer to graph struct read in.
 */
Graph* readGraphStdin() {
    int n; 
    scanf("%d", &n);
    Graph* G;
    G = malloc(sizeof(Graph));
    initGraph(G, n);
    int i,j,k;
    while (scanf("%d,%d,%d", &i, &j, &k) != EOF) {
        addEdge(G, i - 1, j - 1);
    }
    return G;
}

//Must be reset between each partitioning.
int orderIndex = 0;

/*
 * Name:        bipartiteDFS
 * Purpose:     Performs DFS on graph that partitions graph into two 
 *              bipartitions or returns when odd cycle is found while 
 *              recording traversal ordering.
 * Arguments:   Graph G to attempt to partition, vertex index v_i of starting
 *              vertex, parity to start partitioning with (must be 1 or 0, 
 *              generally won't matter which one) and array of vertices order
 *              where traversal ordering will be recorded.
 * Returns:     1 if all vertices reachable from v_i can be partitioned and
 *              0 otherwise (i.e. a odd cycle was detected).
 */
int bipartiteDFS(Graph *G, int v_i, int parity, vertex **order) {
    G->V[v_i].parity = parity;
    G->V[v_i].seen = 1;
    order[orderIndex] = &G->V[v_i];
    orderIndex++;
    int i;
    for (i = 0; i < G->V[v_i].degree; i++) {
        if (!G->V[v_i].adj[i]->seen) {
            if (!bipartiteDFS(G, G->V[v_i].adj[i]->vertexNum, !parity, order))
                return 0;
        }
        else if (G->V[v_i].adj[i]->parity == parity) {
            order[orderIndex] = G->V[v_i].adj[i];
            return 0;
        }
    }
    return 1;
}

/*
 * Name:        printOddCycle
 * Purpose:        Finds and prints odd cycle given a bipartite DFS traversal
 *              ordering.
 * Arguments:   Array of vertices in order of bipartite DFS traversal.
 */
void printOddCycle(vertex **order) {
    int endVertex = order[orderIndex]->vertexNum;
    int k = orderIndex - 1;
    printf("%d ", endVertex + 1);
    while (order[k]->vertexNum != endVertex) {
        printf("%d ", order[k]->vertexNum + 1);
        k--;
    }
    printf("\n");
}

/*
 * Name:        orderedIsBipartite
 * Purpose:     Attempts to partiton graph into two bipartitions while also
 *              while also testing if graph is bipartitie.
 * Arguments:   Graph G to perform partitioning and array in which the order
 *                      of the graph traversal is recoreded.
 * Returns:     1 if graph is bipartite, 0 otherwise.
 */
int orderedIsBipartite(Graph *G, vertex **order) {
    int i;
    for (i = 0; i < G->n; i++) {
        if (!G->V[i].seen) {
            orderIndex = 0;
            if (!bipartiteDFS(G, i, 0, order))
                return 0;
        }
    }
    return 1;
}

/*
 * Name:        printPartition
 * Purpose:     Prints partitions of bipartite graph after partititoning has
 *              been performed on it.
 * Arguments:   Graph G
 */
void printPartitions(Graph *G) {
    int i;
    printf("V1: ");
    for (i = 0; i < G->n; i++) {
        if (G->V[i].parity)
            printf("%d ", G->V[i].vertexNum + 1);
    }
    printf("\nV2: ");
    for (i = 0; i < G->n; i++) {
        if (!G->V[i].parity)
            printf("%d ", G->V[i].vertexNum + 1);
    }
    printf("\n");
}

int main() {
    Graph* G = readGraphStdin();
    vertex **order = malloc(sizeof(vertex*) * G->n + 1);
    if (orderedIsBipartite(G, order)) {
        printf("Bipartite: the partitions are:\n");
        printPartitions(G);
    }
    else {
        printf("Not bipartite; an odd cycle is\n");
        printOddCycle(order);
    }
}
