
import math
from math import sqrt, isclose
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
    def vec(cls, x, y):
        return PVec(x, y, True)

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
            return PVec(0, 1, True)
        else:
            d = sqrt(1+slope**2)
            return PVec(1/d, slope/d, True)

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
    def parallel(self, l2):
        return isclose(self.slope(), l2.slope())

    def __str__(self):
        return f'[Line through {self.p} slope {self.slope():.2f}]'

class Segment():
    def __init__(self, p1, p2):
        p1.expect_point()
        p2.expect_point()
        self.p1 = p1
        self.p2 = p2

    def line(self):
        return Line(self.p1, self.p2)

    def length(self):
        return self.p1.distance(self.p2)

    def slope(self):
        return self.line().slope()

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

if __name__ == '__main__':
    # ln = Line(PVec.point(0,0), PVec.point(1,1))
    # for i in range(30):
    #     p = PVec.point(1.2, i/10)
    #     if ln.contains(p):
    #         print(f"The line {ln} contains point {p}")
    #         print(f"Its parameter is {ln.param(p):.2f}")
    p1 = PVec.point(5,12)
    p2 = PVec.point(7,6)
    s = Segment(p1, p2)
    print(s, s.midpoint())
    print("length", s.length())
    print("pbis", s.perpendicular_bisector())
