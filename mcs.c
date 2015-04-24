/*
 * File:        mcs.c
 * Author:      Tom Hadlaw 100101188
 * Date:        15/02/2015
 * Version:     1.0
 * Purpose:     Performs a maximum cardinality search on a graph and gives
 *              a vertex ordering such that a greedy coloring will produce
 *              an optimal graph coloring.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Vertex {
    int label;
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
    }
}

/*
 * Name:        addEdge
 * Purpose:     Adds edge ViVi to graph G.
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
 * Name:        maximumCardinalitySearch
 * Purpose:     Performs a maximum cardinality search.
 * Arguments:   Graph G to perform mcs on.
 * Returns:     Array of vertex pointers ordered by the maximum cardinality 
 *              order.
 */
vertex** maximumCardinalitySearch(Graph G) {
    int n = G.n;
    vertex** ordv;
    ordv = malloc(sizeof(vertex*) * n);
    int visited = 0;
    while (visited < n) {
        int maxlabel = -1;
        vertex *maxv = NULL;
        int i;
        for (i = 0; i < n; i++) {
            if (G.V[i].label > maxlabel && G.V[i].visited != 1) {
                maxlabel = G.V[i].label;
                maxv = &G.V[i];
            }
        }
        for (i = 0; i < maxv->degree; i++) {
            maxv->adj[i]->label++;
        }
        maxv->visited = 1;
        ordv[visited] = maxv;
        visited++;
    }
    return ordv;
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

/*
 * Name:        greedyColoring
 * Purpose:     Performs greedy coloring on graph given an ordering.
 */
void greedyColoring(Graph *G, vertex** order) {
    int i;
    int availableColors[G->maxDegree + 1];
    for (i = 0; i < G->n; i++) {
        memset(availableColors, 0, (G->maxDegree + 1) * sizeof(int));
        int k;
        for (k = 0; k < order[i]->degree; k++) {
            if (order[i]->adj[k]->color != -1) {
                availableColors[order[i]->adj[k]->color] = 1;
            }
        }
        for (k = 0; k < G->maxDegree + 1; k++) {
            if (availableColors[k] == 0) {
                order[i]->color = k; 
                break;
            }
        }
    }
}

int main() {
    Graph* G = readGraphStdin();
    vertex** order = maximumCardinalitySearch(*G);
    greedyColoring(G, order);
    printf("The greedy-colouring-is-optimal ordering of the vertices is\n");
    int i;
    for (i = 0; i < G->n; i++)
        printf("%d, %d\n", order[i]->vertexNum + 1, order[i]->color + 1);
}
