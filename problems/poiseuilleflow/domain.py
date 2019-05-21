from solver import *

class Domain(BaseDomain):
    defaults = {**BaseDomain.defaults, **dict(
        h = 1.0,
        l = 1.0,
    )}

    def geometry(self):
        self.shapes.append(
            self.geom.add_polygon([
                [0, 0, 0], 
                [self.l, 0, 0], 
                [self.l, self.h, 0], 
                [0, self.h, 0]
            ]),
        )
        # self.geom.set_transfinite_surface(self.shapes[-1].surface, size=[1.0/self.cellsize/self.cellscale, 1.0/self.cellsize/self.cellscale], orientation='Alternate')
