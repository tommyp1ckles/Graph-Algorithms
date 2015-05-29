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