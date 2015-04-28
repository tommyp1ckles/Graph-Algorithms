class Vertex:
    seen = False
    vertexNum = None

class DiGraph():
    V = None
    n = 0
    adj = list()
    weights = dict() # Contains both the weights and the flows.
    def __init__(self, N):
        self.V = list()
        self.adj = [[]] * 10
        for i in xrange(0, N):
            self.V.append(Vertex())
            self.V[i].vertexNum = i
    def addEdge(self, i, j, weight):
        self.adj[i].append(self.V[j])
        self.weights[str(i) + "," + str(j)] = [0, weight]
    def setFlow(self, i, j, flow):
        self.weights[str(i) + "," + str(j)][0] = flow
    def getWeight(self, i, j):
        return self.weights[str(i) + "," + str(j)][1]
    def getFlow(self, i, j):
        return self.weights[str(i) + "," + str(j)][0]

def maxFlow(G, s, t):
    R = set([G.V[s]])
    S = set()
    print R
    print S

G = DiGraph(4)
maxFlow(G, 0, 1)
