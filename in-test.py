
import voronoi.geom as g

from math import isclose, sin, cos, pi

vertices = [ g.PVec.point(2*sin(2*pi*th), 2*cos(2*pi*th))
             for th in [ x/7.0 for x in range(7) ] ]
print(vertices)

# We have a polygon defined by a list of vertices
# Starting from point p, search rightward
# for intersections with any of the edges of the polygon
# and return the count of the number of such intersections.
def raycast(vs, p):
#    import pdb; pdb.set_trace()

    prev = vs[-1]
    count = 0
    for cur in vs:
        edge = g.Segment(prev, cur)
        ray = g.Ray(p, g.PVec.vec(1, 0))
#        ch = '.'
        if ray.intersects(edge):
            count += 1
            ch = 'x'
        prev = cur
#        print(ch,end='')
    return count

def contains(vs, p):
    """Is point p in the square?"""
#    import pdb; pdb.set_trace()
    return raycast(vs, p) % 2 == 0

#print(raycast(vertices, g.PVec.point(0,1)))
#exit(0)

y = x = -3.0

#print(contains(vertices, g.PVec.point(0.1,0.1)))

while y <= 3.0:
    x = -3.0
    while x <= 3.0:
        ch = '.'
        if contains(vertices, g.PVec.point(x, y)):
            ch = "*"
        print(ch, end="")
        x += 0.06
#    print(f"y={y:.1f}", end="")
#    ch = raycast(vertices, g.PVec.point(-10, y))
    print()
    y += 0.2
#    print()
