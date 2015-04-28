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
    adj = list()
    incEdges = list() #Maintaining list of incoming edges should speed
    #up certain algorithms.
    weights = dict() # Contains both the weights and the flows.
    def __init__(self, N):
        self.V = list()
        self.adj = [[]] * N
        self.incEdges = [[]] * N
        for i in xrange(0, N):
            self.V.append(Vertex())
            self.V[i].vertexNum = i
    def addEdge(self, i, j, weight):
        self.adj[i].append(self.V[j])
        self.incEdges[j].append(self.V[i])
        self.weights[str(i) + "," + str(j)] = [0, weight]
    def setFlow(self, i, j, flow):
        self.weights[str(i) + "," + str(j)][0] = flow
    def getWeight(self, i, j):
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

def maxFlow(G, s, t):
    if not isinstance(G, DiGraph):
        raise TypeError( \
            "maxFlow requires a DiGraph " + \
            "(directed graph).")
    R = set([G.V[s]])
    S = set()
    #while True:
    v = (R - S).pop()
    print v

G = DiGraph(3)
G.addEdge(0,1,111)
G.addEdge(1,2,222)
G.addEdge(2,0,333)
G.printGraph()
