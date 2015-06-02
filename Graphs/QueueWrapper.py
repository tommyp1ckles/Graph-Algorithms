import Queue

#TODO: Reimplement this yourself instead of just a wrapper for pythons shitty
# PriorityQueue class.
class pqueue:
    Q = None
    n = None
    maxSize = None
    def __init__(self, size):
        self.maxSize = size
        self.Q = Queue.PriorityQueue(maxsize=size)
        self.n = 0
    def push(self, element):
        if self.n is self.maxSize:
            return False
        self.Q.put(element)
        self.n = self.n + 1
        return True
    def pop(self):
        if self.n is 0:
            return False
        self.n = self.n - 1
        return self.Q.get()
    def size(self):
        return self.n
    def __str__(self):
        return str(self.Q)
