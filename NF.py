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

    #if not isinstance(G, DiGraph):
    #    raise TypeError( \
    #        "maxFlow requires a DiGraph " + \
    #        "(directed graph).")

def flowAP(G, s, t):
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
        print "*" * 30
        print t_reached
        print reaching
        print str("R = ") + str(R)
        print str("S = ") + str(S)
        print "*" * 30
        S.add(v)
        if R is S:
            return None
        v = (R - S).pop()
    print "->" + str(traceAPFlowPath(G, s, t, reaching))
    return (t_reached, reaching, R, S)

def traceAPFlowPath(G, s, t, reaching, order = []):
    curr = t
    order = [curr]
    min_cap = G.getWeight(curr, reaching[curr]) - G.getFlow(curr, reaching[curr])
    while curr != s:
        edge_excess = G.getWeight(curr, reaching[curr]) - G.getFlow(curr, reaching[curr])
        if edge_excess < min_cap:
            min_cap = edge_excess
        curr = reaching[curr]
        order.append(curr)
    return (order, min_cap)

G = DiGraph(4)
G.addEdge(0,1,1)
G.addEdge(1,2,2)
G.addEdge(2,3,1)
flowAP(G, 0, 3)
