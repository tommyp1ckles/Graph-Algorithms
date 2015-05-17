import sys
from numpy import *
import Graphs

############################################################
import cProfile
############################################################

def edgeWeight(G, i, j):
    key = "%d,%d" % (i, j)
    if key in G.weights:
        return G.weights[key][1]
    else:
        return None

def edgeFlow(G, i, j):
    key = "%d,%d" % (i, j)
    if key in G.weights:
        return G.weights[key][0]
    else:
        return None

def netFlow(G, i, j):
    f = edgeFlow(G, i, j)
    if f is not None:
        return f
    else:
        return edgeFlow(G, j, i)

def netWeight(G, i, j):
    f = edgeWeight(G, i, j)
    if f is not None:
        return f
    else:
        return edgeWeight(G, j, i)

def flowAP(G, s, t):
    reaching = zeros(G.n, dtype=int64)
    reaching.fill(-1)
    R = set([G.V[s]])
    S = set()
    t_reached = False
    v = (R - S).pop()
    while not t_reached:
        for w in G.adj[v.vertexNum]:
            if edgeFlow(G, v.vertexNum, w.vertexNum) < \
                    edgeWeight(G, v.vertexNum, w.vertexNum):
                reaching[w.vertexNum] = v.vertexNum
                R.add(w)
                if w.vertexNum is t:
                    t_reached = True
        for w in G.inc[v.vertexNum]:
            if edgeFlow(G, w.vertexNum, v.vertexNum) > 0:
                reaching[w.vertexNum] = v.vertexNum
                R.add(w)
                if w.vertexNum is t:
                    t_reached = True
        S.add(v)
        if R == S:
            return None
        v = (R - S).pop()
    return reaching

def traceAPFlowPath(G, s, t, reaching):
    curr = t
    order = [curr]
    min_cap = netWeight(G, curr, reaching[curr]) - netFlow(G, curr, reaching[curr])
    if ("%d,%d" % (curr,reaching[curr])) in G.weights:
        forward = [False]
    else:
        forward = [True]
    while curr != s:
        edge_excess = netWeight(G, curr, reaching[curr]) - netFlow(G, curr, reaching[curr])
        if edge_excess < min_cap:
            min_cap = edge_excess
        if ("%d,%d" % (curr,reaching[curr])) in G.weights:
            forward.append(False)
        else:
            forward.append(True)
        curr = reaching[curr]
        order.append(curr)
    return (order, min_cap, forward)

def maxFlow(G, s, t):
    if not isinstance(G, Graphs.DiGraph):
        raise TypeError( \
            "maxFlow requires a DiGraph " + \
            "(directed graph).")
    AP_reaching = flowAP(G, s, t)
    if AP_reaching is None:
        return
    while AP_reaching is not None:
        path_order_tuple = traceAPFlowPath(G, s, t, AP_reaching)
        order = path_order_tuple[0]
        min_cap = path_order_tuple[1]
        for k in xrange(0, len(order) - 1):
            i = order[k]
            j = order[k+1]
            is_forward = path_order_tuple[2][k]
            if ("%d,%d" % (i,j)) in G.weights:
                if not is_foward:
                    min_cap = min_cap * -1
                G.weights["%d,%d" % (i,j)][0] = \
                        G.weights["%d,%d" % (i,j)][0] + min_cap
            else:
                if not is_forward:
                    min_cap = min_cap * -1
                G.weights["%d,%d" % (j,i)][0] = \
                        G.weights["%d,%d" % (j,i)][0] + min_cap
        AP_reaching = flowAP(G, s, t)
    return G.getIncomingFlow(t)


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
    G = Graphs.Graph(n)
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

def resetVertices(G):
    """Resets 'seen' attribute in all the vertices of a graph"""
    for v in G.V:
        v.seen = False

def bipartiteDFS(G, v, vertex_parity, parity = True):
    vertex_parity = [None] * G.n
    for u in G.adj[v]:
        if u.seen and vertexParity[u.vertexNum] is parity:
                return False
        else:
            bipartiteDFS(G, u,vertexNum, vertexParity, (not parity))

def isBipartite(G):
    """Checks to see if graph is bipartite"""
    for v in G.V:
        if not v.seen:
            if not bipartiteDFS(G, v.vertexNum, [None] * G.n)
                return False
    return True

G = Graphs.Graph(4)

#G = importGraphStdin()
#MM(G)

#G = Graphs.DiGraph(4)
#G.addEdge(0,1,1000000000)
#G.addEdge(0,2,1000000000)
#G.addEdge(1,2,1)
#G.addEdge(1,3,1000000000)
#G.addEdge(2,3,1000000000)
#print maxFlow(G, 0, 3)
#print "********" + str(G.weights["0,1"][0])
