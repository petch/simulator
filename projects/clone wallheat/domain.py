from solver import *

class Domain(BaseDomain):
    defaults = {**BaseDomain.defaults, **dict(
        h  = 1.0,
        l1 = 0.5,
        l2 = 1.0
    )}

    def geometry(self):
        s1 = self.geom.add_polygon([
            [0, 0, 0], 
            [self.l1, 0, 0], 
            [self.l1, self.h, 0], 
            [0, self.h, 0]
        ])
        s2 = self.geom.add_polygon([
            [self.l1, 0, 0], 
            [self.l2, 0, 0], 
            [self.l2, self.h, 0], 
            [self.l1, self.h, 0]
        ])
        self.shapes += [s1, s2]
