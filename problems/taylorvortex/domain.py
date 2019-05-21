from solver import *

class Domain(BaseDomain):
    defaults = {**BaseDomain.defaults, **dict(
        sx = -0.5,
        sy = -0.5,
        ex = 0.5,
        ey = 0.5,
    )}

    def geometry(self):
        self.shapes.append(
            self.geom.add_polygon([
                [self.sx, self.sy, 0], 
                [self.ex, self.sy, 0], 
                [self.ex, self.ey, 0], 
                [self.sx, self.ey, 0]
            ]),
        )
