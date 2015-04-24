#!/usr/bin/python

# File:         MWM.py
# Author:       Tom Hadlaw
# Date:         2015/01/21
# Version:      1.0
# Purpose:      Reads in a text file containing graph data for a complete
#               bipartite graph and finds a maximum weighted matching for
#               the graph.

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
    label = None
    maxW = -1
    partition = None
#Graph object: represents a general graph, constructor method takes size of
#graph n and edges are added using addEdge(i, j) method. Also implements some
#other methods which I never really used but may become useful one day.
class Graph():
    """Represents a general unweighted Graph"""
    #V = [] #start with empty vertex set
    V = None
    n = 0
    Adj = None #Adjacency list
    W = {}
    def __init__(self, N):
        """Constructor method
        Args:
            param1 (N): Size of the graph.
        """

        self.V = []
        #self.V = zeros(dtype=Vertex()
        self.Adj = []
        for i in range(0, N):
            self.Adj.append([])
            self.V.append(Vertex())
            self.V[i].maxW = -1
            self.V[i].vertexNum = i
            self.n = N
        #self.V = []
        """
        l = []
        for i in range(0, N):
            l.append(Vertex())
        self.V = array(l)
        self.Adj = []
        for i in range(0, N):
            self.Adj.append([])
            #self.V.append(Vertex())
            self.V[i].maxW = -1
            self.V[i].vertexNum = i
            self.n = N
        """
    def addEdge(self, i, j, w):
        """Adds edge from vertex i to vertex j to graph
        Args:
            param1 (i): pairwise adjacent vertex i.
            param2 (j): pairwise adjacent vertex j.
            param3 (w): weight of edge.
        """
        #print "adding edge: " + str(i) + "," + str(j) + " == " + str(w)
        self.Adj[i].append(self.V[j])
        self.Adj[j].append(self.V[i])
        if i < j:
            self.W[str(i) + "," + str(j)] = w
        else:
            self.W[str(j) + "," + str(i)] = w
        if w > self.V[i].maxW:
            self.V[i].maxW = w
        if w > self.V[j].maxW:
            self.V[j].maxW = w

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
    if sys.getrecursionlimit() <= n:
        sys.setrecursionlimit(n * 10) #Should probably figure this out.
    for line in sys.stdin:
        arr = line.split(",")
        G.addEdge(int(arr[0]) - 1, int(arr[1]) - 1, int(arr[2]))
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
    """Performs maximum matching algorithm (This is just A1).
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
        for v in G.V:
            v.seen = False
        P = AP(G, M, vi)
        Ps = []
        if P is not None:
            for i in range(0, len(P) - 1):
                Ps.append(P[i])
                Ps.append(P[i+1])
        else:
            Ps = [vi, G.n+1]
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


def m():
    """Performs maximum matching algorithm.
    Args:
        param1 (G): Graph G to find maximum matching on.
    Modifies: Vertex objects in G have values changed.
    Outputs: Prints what edges are matched with what (in ascending order of
        vertex index if matching is found, prints that no matching has been
        found otherwise.
    Assumptions: G is bipartite.
    """
    G = importGraphStdin()
    M = []
    vi = getUnsaturated(G, edgeSet(M))
    while not vi == G.n:
        for v in G.V:
            v.seen = False
        P = AP(G, M, vi)
        Ps = []
        if P is not None:
            for i in range(0, len(P) - 1):
                Ps.append(P[i])
                Ps.append(P[i+1])
        else:
            Ps = [vi, G.n+1]
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

def w(G, i, j):
    """Gets weight of edge ij in graph G.
    Arguments:  param1(G): Graph G.
                param2(i): Vertex index i from ij edge.
                param2(i): Vertex index j from ij edge.
    Returns:    Weight of edge.
    """
    if (i < j):
        return G.W[str(i) + "," + str(j)]
    else:
        return G.W[str(j) + "," + str(i)]


def partition(G, i, S1, S2, depth = 0):
    """Partitions bipartite graph G into two independent sets.
    Purpose:    Partitions vertices of bipartite graph into two disjoint
                    sets by putting them in lists S1 and S2 as well as marking
                    each vertex by what set it belongs to.
    Arguments:  param1(G): Graph G.
                param2(i): Starting vertex index (can be anything really).
                param3(S1): Empty set 1.
                param4(S2): Empty set 2.
                param5(depth): Leave this be.
    """
    for v in G.Adj[i]:
        if not v.seen:
            if depth % 2 == 0:
                S1.append(v)
                v.partition = 1
            else:
                S2.append(v)
                v.partition = 2
            v.seen = True
            partition(G, v.vertexNum, S1, S2, depth + 1)

#Note: All vertices have to be preset to v.seen = false (unseen)
def createTrivialLabel(G):
    """Labels G with a trivial feasible label (Max weights on top and 0s on
        bottom)"
    Arguments:  param1(G): Graph G.
    """
    S1 = []
    S2 = []
    partition(G, 0, S1, S2)
    for v in S1:
        v.label = v.maxW
    for v in S2:
        v.label = 0

def resetVertices(G):
    """Sets of vertices of G to unseen.
    Arguments:  param1(G): Graph G.
    """
    for v in G.V:
        v.seen = False

def createEqualitySubgraph(G):
    """Creates equality subgraph of labeled graph G.
    Arguments:  param1(G): Graph G.
    Returns:    Equality Subgraph of G.
    """
    Gl = Graph(G.n)
    resetVertices(G)
    for u in G.V:
        if u.partition is 1:
            for v in G.Adj[u.vertexNum]:
                if w(G, u.vertexNum, v.vertexNum) == u.label + v.label and not v.seen:
                    Gl.addEdge(u.vertexNum, v.vertexNum, w(G, u.vertexNum, v.vertexNum))
            u.seen = True
    return Gl

def testForMM(G):
    """Finds maximum matching on graph G.
    Arguments:  param1: Graph G.
    Returns: Matching M (unmatched edges matched with n+1th edge.
    """
    M = []
    vi = getUnsaturated(G, edgeSet(M))
    while not vi == G.n:
        for v in G.V:
            v.seen = False
        P = AP(G, M, vi)
        Ps = []
        if P is not None:
            for i in range(0, len(P) - 1):
                Ps.append(P[i])
                Ps.append(P[i+1])
        else:
            Ps = [vi, G.n+1]
        M_prime = edgeSet(M).symmetric_difference(edgeSet(Ps))
        M = vertexList(M_prime)
        vi = getUnsaturated(G, edgeSet(M))
    return M

def w(G, i, j):
    """Returns weight of edge ij in graph G.
    Arguments:  param1(G): Graph G.
                param2(i): Vertex i of pairwise edge.
                param3(j): Vertex j of pairwise edge.
    Returns:    Weight of edge.
    """
    if (i < j):
        return G.W[str(i) + "," + str(j)]
    else:
        return G.W[str(j) + "," + str(i)]

def getAlpha(G, S, NS):
    """Finds alpha value
    Purpose: Finds min(l(v) + l(u) - w(uv)) where v are elem in S and u
            are elem in N(S).
    Arguments:  param1(G): Graph G.
                param2(S): Set S.
                param3(NS): Neighborhood of S.
    Returns:    Alpha value.
    """
    alpha = None
    for u in S:
        for v in G.Adj[u]:
            if v.vertexNum not in NS:
                val = G.V[u].label + G.V[v.vertexNum].label - \
                        w(G, u, v.vertexNum)
                if val < alpha or alpha is None:
                    #if val > 0:
                    alpha = val
    return alpha

def toggleLabels(G, S, NS, alpha):
    """Toggles the labels of sets S/N(S) gvien a alpha value.
    Purpose: Toggles the labels by subtracting allalpha from elements in S
        and adding to elements of N(S) in order to increase matching size on
        equality subgraph.
    Arguments"  param1(G): Graph G.
                param2(S): Set of vertices S.
                param3(NS): Neighborhood of S (N(S)).
                param4(alpha): Alpha value to use for toggling.
    """
    for v in S:
        G.V[v].label = G.V[v].label - alpha
    for v in NS:
        G.V[v].label = G.V[v].label + alpha

def testForAP(G, M, v, SNS):
    """Finds a set of vertices that cannot be matched (by Halls thm.).
    Purpose:    Given a unmatched vertex index and matching finds a set of
                vertices that has the property that it can be partitioned into
                sets S and N(S) such that |S| > |N(S)|.
    Arguments:  param1(G): Graph G.
                param2(M): Matching M.
                param3(v): Index of unmatched vertex.
                param4(SNS): Empty list that is populated with elements of
                    S and N(S).
    Returns:    None if such a set cannot be found.
    """
    for w in G.Adj[v]:
        if not w.seen:
            if w.vertexNum in M:
                w.seen = True
                w_prime = M.index(w.vertexNum)
                offset = -1
                if w_prime % 2 == 0:
                    offset = 1
                w_prime = M[w_prime + offset]
                SNS.append(w.vertexNum)
                SNS.append(w_prime)
                P = testForAP(G, M, w_prime, SNS)
    return None

def matched(m, unmatched):
    """Removes all unmatched edges from my matching lists.
    Purpose:    Matchings are returned with unmatched vertices being matched
            with the n+1th vertex to signify no match was found, this function
            removes all unmatched entries.
    Argument:   param1(m): Matching list to remove unmatched entries.
                param2(unmatched): Index to which unmatched vertices are paired
                with (n+1)
    Returns:    Matching list of just matched vertices.
    """
    M = []
    for i in range(1, len(m), 2):
        if not m[i] == unmatched:
            M.append(m[i-1])
            M.append(m[i])
    return M

def getSumW(G, m):
    """Finds total sum of weighted matched.
    Arguments:  param1(G): Graph G.
                param2(m): Matching to sum.
    Returns:    Sum of all edge weights in matching.
    """
    sum = 0
    for i in range(0, len(m), 2):
        sum = sum + w(G, m[i], m[i+1])
    return sum

def OMM():
    """Reads in graph and performs maximum weighting matching algorithm on it.
    Outputs: Prints what edges are matched with what (in ascending order of
        first vertex index) and the weight of the corresponding edge.
    Assumptions: G is bipartite.
    """
    G = importGraphStdin()
    createTrivialLabel(G)
    V1 = []
    V2 = []
    resetVertices(G)
    partition(G, 0, V1, V2)
    while True:
        t = time.time()
        Gl = createEqualitySubgraph(G)
        resetVertices(Gl)
        m = testForMM(Gl)
        M = matched(m, G.n + 1)
        unmatched = None
        for i in range(0, len(m)):
            if m[i] >= (G.n+1) and G.V[m[i-1]].partition is 1:
                unmatched = m[i-1]
                break
        if (G.n + 1) not in m:
            #print m
            sortedM = sortMatching(m)
            print "The maximum weight matching has weight " + \
                    str(getSumW(G, m))
            for m in sortedM:
                print "v" + str(m[0] + 1) + " is matched to v" + str(m[1] + 1) + \
                        " (weight " + str(w(G, m[0], m[1])) + ")."
            return
        resetVertices(Gl)
        SNS = []
        P = testForAP(Gl, matched(m, G.n+1), unmatched, SNS)
        SNS = [unmatched] + SNS
        S = []
        NS = []
        for v in SNS:
            if G.V[v].partition is 1:
                S.append(v)
            else:
                NS.append(v)
        alpha = getAlpha(G, S, NS)
        toggleLabels(G, S, NS, alpha)

OMM()
