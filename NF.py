from numpy import *

class Vertex:
    seen = False
    vertexNum = None
    def __str__(self):
        return "<Vertex %d>" % self.vertexNum
    def __repr__(self):
        return "<Vertex %d>" % self.vertexNum

class DiGraph():
    V = None
    n = 0
    adj = []
    inc = [] #Maintaining list of incoming edges should speed
    #up certain algorithms.
    weights = dict() # Contains both the weights and the flows.
    def __init__(self, N):
        self.n = N
        self.V = list()
        for i in xrange(0, N):
            self.adj.append([])
            self.inc.append([])
            self.V.append(Vertex())
            self.V[i].vertexNum = i
    def addEdge(self, i, j, weight):
        self.adj[i].append(self.V[j])
        self.inc[j].append(self.V[i])
        self.weights[str(i) + "," + str(j)] = [0, weight]
    def setFlow(self, i, j, flow):
        self.weights[str(i) + "," + str(j)][0] = flow
    def getWeight(self, i, j):
        print self.weights
        return self.weights[str(i) + "," + str(j)][1]
    def getFlow(self, i, j):
        return self.weights[str(i) + "," + str(j)][0]
    def printGraph(self):
        for v in self.V:
            print "%s ->" % str(v),
            for adjvert in self.adj[v.vertexNum]:
                print " %s" % str(adjvert),
            print
    def __str__(self):
        return "<DiGraph %d>" % self.n
    def __repr__(self):
        return "<DiGraph %d>" % self.n

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

    #if not isinstance(G, DiGraph):
    #    raise TypeError( \
    #        "maxFlow requires a DiGraph " + \
    #        "(directed graph).")

def flowAP(G, s, t):
    print "^^^^"
    print G
    print s
    print t
    print "*****"
    reaching = zeros(G.n, dtype=int64)
    reaching.fill(-1)
    R = set([G.V[s]])
    S = set()
    t_reached = False
    v = (R - S).pop()
    while not t_reached:
        print v
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
        print R
        print S
        v = (R - S).pop()
    #return (t_reached, reaching, R, S)
    return reaching
def traceAPFlowPath(G, s, t, reaching):
    curr = t
    order = [curr]
    #min_cap = edgeWeight(G, curr, reaching[curr]) - G.getFlow(curr, reaching[curr])
    min_cap = netWeight(G, curr, reaching[curr]) - netFlow(G, curr, reaching[curr])
    while curr != s:
        edge_excess = netWeight(G, curr, reaching[curr]) - netFlow(G, curr, reaching[curr])
        if edge_excess < min_cap:
            min_cap = edge_excess
        curr = reaching[curr]
        order.append(curr)
    return (order, min_cap)

def maxFlow(G, s, t):
    AP_reaching = flowAP(G, s, t)
    if AP_reaching is None:
        return
    while AP_reaching is not None:
        path_order_tuple = traceAPFlowPath(G, s, t, AP_reaching)
        order = path_order_tuple[0]
        min_cap = path_order_tuple[1]
        #OOOPs you gotta subtract flow on back edges...
        for k in xrange(0, len(order) - 1):
            i = order[k]
            j = order[k+1]
            if ("%d,%d" % (i,j)) in G.weights:
                G.weights["%d,%d" % (i,j)][0] = \
                        G.weights["%d,%d" % (i,j)][0] + min_cap
                print "adding %d flow." % min_cap
            else:
                G.weights["%d,%d" % (j,i)][0] = \
                        G.weights["%d,%d" % (j,i)][0] + min_cap
                print "adding %d flow." % min_cap
        AP_reaching = flowAP(G, s, t)
    return

G = DiGraph(4)
G.addEdge(0,3,1)
G.addEdge(0,1,1)
G.addEdge(1,2,1)
G.addEdge(2,3,1)
maxFlow(G, 0, 3)
#G.addEdge(0,1,1)
#G.addEdge(0,1,1)
#G.addEdge(1,2,2)
#G.addEdge(2,3,1)
#flowAP(G, 0, 3)
