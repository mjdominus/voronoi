import geom

from math import sqrt, isclose

class Vertex(geom.PVec):
    def __init__(self, point):
        self.x = point.x
        self.y = point.y
        self.isvec = False
        self.edges = []

    def cells(self):
        return set([ e.cells() for e in self.edges ])

class Edge(geom.Segment):
    def __init__(self, seg):
        super().__init__(seg.p1, seg.p2)
        self.cells = set()

class Cell():
    """A cell has a site, which is a point,
    and an ordered sequence of edges."""
    def __init__(self, site, edges):
        n = len(edges)
        if n < 3:
            raise Exception("Cell has only", len(edges), "sides")
        self.s = site
        self.e = edges
        self._check_edge_closure()

    def v(self):
        return [ e.p1 for e in self.edges ]

    def _check_edge_closure(self):
        prev = self.e[-1].p2
        for i in range(self.e):
            cur = self.e[i].p1
            if prev != cur:
                raise Exception(f"edge list not closed: e{i-1}.end = {prev} ≠ {cur} = e{i}.start")
            prev = cur

    def contains(self, p):
        """Is point p in this cell?"""
        total = PVec.zero()
        for v in self.v():
            total += v - p
        return isclose(total.length(), 0)

    def __str__(self):
        cellstr = ", ".join([str(v) for v in self.v ])
        return f'Cell (at {self.s}) vertices [{cellstr}]'
