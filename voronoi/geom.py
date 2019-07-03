
import math
from math import sqrt, isclose, cos, sin, pi
from dataclasses import dataclass

@dataclass
class PVec():
    x: float
    y: float
    isvec: bool

    @classmethod
    def point(cls, x, y):
        return PVec(x, y, False)

    @classmethod
    def point_polar(cls, r, th):
        return cls(r * cos(th), r * sin(th), False)

    @classmethod
    def vec(cls, x, y):
        return cls(x, y, True)

    def is_point(self):
        return not self.isvec

    def is_vector(self):
        return self.isvec

    @classmethod
    def zero(cls):
        return cls(0, 0, True)

    @classmethod
    def unitvec(cls, slope):
        if math.isinf(slope):
            return cls(0, 1, True)
        else:
            d = sqrt(1+slope**2)
            return cls(1/d, slope/d, True)

    def expect_vector(self):
        if not self.isvec:
            raise Exception("vector expected")

    def expect_point(self):
        if self.isvec:
            raise Exception("vector expected")

    def length(self):
        self.expect_vector()
        return sqrt(self.x ** 2 + self.y ** 2)

    def slope(self):
        self.expect_vector()
        if self.x == 0:
            return math.inf
        else:
            return self.y/self.x

    def distance(self, p2):
        self.expect_point()
        p2.expect_point()
        return (self - p2).length()

    def __add__(self, v):
        if self.is_vector():
            return PVec(self.x + v.x, self.y + v.y, v.is_vector()) # same type as v
        elif v.is_vector():
            return PVec(self.x + v.x, self.y + v.y, False) # point
        else:
            raise Exception("Attempt to add two points")

    def __sub__(self, v):
        if self.is_point():
            return PVec(self.x - v.x, self.y - v.y, v.is_point()) # opposite type as v
        elif v.is_vector():
            return PVec(self.x - v.x, self.y - v.y, True) # vector
        else:
            raise Exception("Attempt to subtract point from vector")

    def __mul__(self, s):
        """Multiply vector by scalar"""
        self.expect_vector()
        return PVec(self.x * s, self.y * s, True)
    def __rmul__(self, s):
        return self.__mul__(s)

    def __neg__(self):
        self.expect_vector()
        return self * -1

    def __str__(self):
        if self.is_point():
            return f"({self.x :.1f}, {self.y :.1f})"
        elif self.is_vector():
            return f"<{self.x :.1f}, {self.y :.1f}>"
        else:
            return self.__repr__()

class Line:
    def __init__(self, p1, p2):
        """You can pass two points, or a point and a vector
        in that order."""
        p1.expect_point()
        self.p = p1
        if p2.is_vector():
            self.v = p2
        elif p2.is_point():
            self.v = p2 - p1
        else:
            raise Exception("Expected point or vector")

    def param_ok(self, p):
        return True

    def slope(self):
        return self.v.slope()

    def isvertical(self):
        return math.isinf(self.v.slope())

    def contains(self, p):
        """Does point p lie on this line?"""
        p.expect_point()
        # Maybe it would be better to calculate
        # (p - self.p).y / self.v.y
        # (p - self.p).x / self.v.x
        # and see if they are close?
        return isclose(self.slope(), (self.p - p).slope())

    def point_at(self, t):
        return self.p + t * self.v

    def param(self, p):
        if self.contains(p):
            vv = p - self.p
            if vv.x == 0:
                return vv.y / self.v.y
            else:
                return vv.x / self.v.x
        else:
            raise Exception("Line {self} does not contain expected point {p}")

    def is_parallel(l1, l2):
        return isclose(l1.slope(), l2.slope())

    def intersects(l1, l2):
        p, u1, u2 = l1.intersection_util(l2)
        return l1.param_ok(u1) and l2.param_ok(u2)

    def intersection_util(l1, l2):
        if l1.is_parallel(l2): return None
        def det(a, b, c, d): return a*d - b*c

        pp = l1.p - l2.p
        den = -det(l1.v.x, l2.v.x, l1.v.y, l2.v.y)
        u1 = det(pp.x, l2.v.x, pp.y, l2.v.y) / den
        return ( l1.point_at(u1),
                 u1,
                 det(l1.v.x, pp.x, l1.v.y, pp.y) / den,
                 )

    def __str__(self):
        return f'[Line through {self.p} slope {self.slope():.2f}]'

class Ray(Line):
    def param_ok(self, p):
        return p >= 0

    def __str__(self):
        return f'[Ray from {self.p} in direction {self.v}]'

class Segment(Line):
    def __init__(self, p1, p2):
        p1.expect_point()
        p2.expect_point()
        super().__init__(p1, p2)
        self.p1 = p1
        self.p2 = p2

    def param_ok(self, p):
        return 0 <= p and p <= 1

    def line(self):
        return Line(self.p, self.v)

    def length(self):
        return self.p1.distance(self.p2)

    def midpoint(self):
        return (self.p2 - self.p1) * 0.5 + self.p1

    def length(self):
        return (self.p2 - self.p1).length()

    def perpendicular_bisector(self):
        if self.slope() == 0:
            s = math.inf
        else:
            s = -1.0 / self.slope()
        return Line(self.midpoint(), PVec.unitvec(s))

    def __str__(self):
        return f'[Segment {self.p1} to {self.p2}]'
