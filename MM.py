#!/usr/bin/python

# File:         MM.py
# Author:       Tom Hadlaw
# Date:         2015/01/21
# Version:      1.0
# Purpose:      Reads in a text file containing graph data for a bipartite
#               and finds a maximum matching for the graph.

import sys
import time

#Vertex object: represents a vertex in the graph.
class Vertex:
    """Represents a single vertex."""
        # A comment not part of the docstring could go here.
    seen = False #vertices are marked "unseen" or "unexamined" by default.
    even = None
    vertexNum = None
    isMatched = False

#Graph object: represents a general graph, constructor method takes size of
#graph n and edges are added using addEdge(i, j) method. Also implements some
#other methods which I never really used but may become useful one day.
class Graph():
    """Represents a general unweighted Graph"""
    V = [] #start with empty vertex set
    n = 0
    Adj = [] #Adjacency list
    Adjl = [] #Adjacency list by label
    def __init__(self, N):
        """Constructor method
        Args:
            param1 (N): Size of the graph.
        """
        for i in range(0, N):
            self.Adj.append([])
            #self.Weight.append([])
            self.V.append(Vertex())
            self.V[i].vertexNum = i
            self.n = N
    def addEdge(self, i, j):
        """Adds edge from vertex i to vertex j to graph
        Args:
          param1 (i): pairwise adjacent vertex i.
          param2 (j): pairwise adjacent vertex j.

        """
        self.Adj[i].append(self.V[j])
        self.Adj[j].append(self.V[i])
    def printAdjList(self):
        """Prints adjacency list for graph"""
        for i in range(0, self.n):
            print "V_" + str(i) + " ---> {" + str(self.Adj[i]) + "}"


def AP(G, M, v):
    """Calculate the distance which a projectile will travel.
    Purpose:     (If the one-liner doesn't describe things well
                     enough, give more description here.  Otherwise
                     you can omit this part of the docstring.)
    Args:
        param1 (G): Graph G
        param2 (M): Current matching.
        param3 (v): Vertex index to find AP on.

    Returns:     Augmenting path in the form of a list of vertices in the path
                    {v1, v2, ... vk} or returns None if no augmenting path
                    possible on that vertex.
    Assumptions: v is unmatched,
        Modifies:    nothing.
        Outputs:     nothing.
    """
    P = [v]
    for w in G.Adj[v]:
        if not w.seen and not w.isMatched:
            w.seen = True
            if w.vertexNum not in M:
                return [v, w.vertexNum]
            else:
                w_prime = M.index(w.vertexNum)
                offset = -1
                if w_prime % 2 == 0:
                    offset = 1
                w_prime = M[w_prime + offset]
                P = AP(G, M, w_prime)
                if P is not None:
                    del P[0]
                    return [v, w.vertexNum, w_prime] + P
def importGraphFile(filename):
    """Reads in graph data from file and returns a graph object.
    Args:
        param1 (filename): String of filename to read graph data from.
    Returns:    Graph containing the read in edges.
    Assumptions:First line in file is an integer representing the n = size
                    of the graph, all lines after that contain edges in the
                    form i,j.
    Notes:      Ignores edge weights parameters.
    """
    f = open(filename, "r")
    n = int(f.readline())
    G = Graph(n)
    sys.setrecursionlimit(n + 1)
    count = 0
    for line in f:
        count += 1
        arr = line.split(",")
        G.addEdge(int(arr[0]) - 1, int(arr[1]) - 1)
    return G

def importGraphStdin():
    """Reads in graph data from stdin and returns a graph object.
    Returns:    Graph containing the read in edges.
    Assumptions:First line in file is an integer representing the n = size
                    of the graph, all lines after that contain edges in the
                    form i,j.
    Notes:      Ignores edge weights parameters.
    """
    n = int(sys.stdin.readline())
    G = Graph(n)
    sys.setrecursionlimit(n + 1)
    count = 0
    for line in sys.stdin:
        count += 1
        arr = line.split(",")
        G.addEdge(int(arr[0]) - 1, int(arr[1]) - 1)
    return G

def edgeSet(L):
    """Converts list of vertices to set of edges
    Args:
        param1 (L): List to be converted.
    Returns:
        Set containing edge tuples (sorted by vertex index).
    """
    S = set()
    for i in range(0, len(L), 2):
        if L[i] < L[i + 1]:
            S.add((L[i], L[i+1]))
        else:
            S.add((L[i+1], L[i]))
    return S

def vertexList(S):
    """Converts set of edges to list of vertices
    Args:
        param1 (S): Set to be converted.
    Returns:
        List of vertices representing edges where the pairs correspond
            to every even/odd pair in the list.
    """
    L = []
    for e in S:
        L.append(e[0])
        L.append(e[1])
    return L
def getUnsaturated(G, M):
    """Returns edge unsaturated by M in G
    Args:
        param1 (G): Graph G.
        param2 (M): Matching M.
    Returns:
        Index of unsaturated vertex from 0...n-1, returns n if no unmatched
        edges where found.
    """
    n = G.n
    sat = [False] * (n + 1)
    for e in M:
        if not e[0] == G.n+1:
            sat[e[0]] = True
        if not e[1] == G.n+1:
            sat[e[1]] = True
    return sat.index(False)

def sortMatching(M):
    """Sorts Set of edges according to first edge in all edge tuple pairs.
    Args:
        param1 (M): Matching M to sort.
    Modifies: Matching M by sorting it (still the same edges).
    """
    S = edgeSet(M)
    l = list(S)
    l.sort()
    return l

def MM(G):
    """Performs maximum matching algorithm.
    Args:
        param1 (G): Graph G to find maximum matching on.
    Modifies: Vertex objects in G have values changed.
    Outputs: Prints what edges are matched with what (in ascending order of
        vertex index if matching is found, prints that no matching has been
        found otherwise.
    Assumptions: G is bipartite.
    """
    M = []
    vi = getUnsaturated(G, edgeSet(M))
    while not vi == G.n:
        #print "v = " + str(vi)
        for v in G.V:
            v.seen = False
        P = AP(G, M, vi)
        #print P
        Ps = []
        #if P is None:
        #    print "None"
        #    return
        if P is not None:
            for i in range(0, len(P) - 1):
                Ps.append(P[i])
                Ps.append(P[i+1])
        else:
            Ps = [vi, G.n+1] #unmatched vertices get matched to the "n+1th"
            #vertex because im terrible at reading assigments before I start
            #them.
        M_prime = edgeSet(M).symmetric_difference(edgeSet(Ps))
        M = vertexList(M_prime)
        vi = getUnsaturated(G, edgeSet(M))
    maxM = map(lambda n: n + 1, M)
    sortedEdges = sortMatching(maxM)
    for edge in sortedEdges:
        if edge[1] != G.n+2:
            print "v%d is matched to v%d." % (edge[0], edge[1])
        else:
            print "v%d is matched to nothing" % edge[0]
    print "number of vertices matched = " + str(len(maxM))

G = importGraphStdin()
MM(G)
