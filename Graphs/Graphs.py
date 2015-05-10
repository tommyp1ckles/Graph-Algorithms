from numpy import *

class Vertex:
    """Represents a single vertex of a graph
    Attributes:
        vertexNum: Number of the vertex, as is stored in graph vertex list.
    """
    seen = False
    vertexNum = None
    def __str__(self):
        return "<Vertex %d>" % self.vertexNum
    def __repr__(self):
        return "<Vertex %d>" % self.vertexNum

class DiGraph():
    """Represents a weighted directed graph with optional edge flows
    Attributes:
        V: List of vertex objects in graph.
        n: Size of the vertex set of the graph.
        adj: Adjacency List of the graph.
        inc: Lists incoming directed edges for each of the vertices.
        weights: Lookup for flow and weight (capacity) of edge.
    """
    V = None
    n = None
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
        return self.weights[str(i) + "," + str(j)][1]
    def getFlow(self, i, j):
        return self.weights[str(i) + "," + str(j)][0]
    def printGraph(self):
        for v in self.V:
            print "%s ->" % str(v),
            for adjvert in self.adj[v.vertexNum]:
                print " %s" % str(adjvert),
            print
    def getIncomingFlow(self, v):
        inc = self.inc[v]
        flow_sum = 0
        for u in inc:
            flow_sum = flow_sum + self.weights["%d,%d" % (u.vertexNum, v)][0]
        return flow_sum
    def __str__(self):
        return "<DiGraph %d>" % self.n
    def __repr__(self):
        return "<DiGraph %d>" % self.n

