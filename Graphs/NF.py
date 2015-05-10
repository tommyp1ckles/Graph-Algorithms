from numpy import *
import Graphs

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

G = Graphs.DiGraph(5)
G.addEdge(0,3,1000000)
G.addEdge(0,4,1000000)
G.addEdge(4,3,666)
G.addEdge(0,1,1)
G.addEdge(1,2,1)
G.addEdge(2,3,1)
print maxFlow(G, 0, 3)
print "********" + str(G.weights["0,3"][0])
print "********" + str(G.weights["2,3"][0])
print "********" + str(G.weights["0,4"][0])
#G.addEdge(0,1,1)
#G.addEdge(0,1,1)
#G.addEdge(1,2,2)
#G.addEdge(2,3,1)
#flowAP(G, 0, 3)
