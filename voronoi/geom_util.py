#!/usr/bin/python3

import voronoi.geom as g

def deg(th):
    return th * pi / 180

def segments(vertices, cycle=True):
    seg = [ g.Segment(vertices[i], vertices[i+1]) for i in range(vertices) ]
    if cycle:
        seg.append(g.Segment(vertices[i-1], vertices[0]))
    return seg

def frange(start, stop, spacing):
    cur = start
    while cur < stop:
        yield cur
        cur += spacing
    return

def point(*args, **kwargs):
    return g.PVec.point(*args, **kwargs)

def vec(*args, **kwargs):
    return g.PVec.vec(*args, **kwargs)
