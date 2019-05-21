from solver import *

class Domain(BaseDomain):
    defaults = {**BaseDomain.defaults, **dict(
        inflow_h = 0.2,
        inflow_l = 0.4,
        outflow_h = 0.4,
        outflow_l = 0.4,
        between_l = 0.2
    )}

    def geometry(self):
        self.shapes.append(
            self.geom.add_polygon([
                [0, 0, 0], 
                [self.inflow_l + self.between_l + self.outflow_l, 0, 0], 
                [self.inflow_l + self.between_l + self.outflow_l, self.outflow_h, 0], 
                [self.inflow_l + self.between_l, self.outflow_h, 0], 
                [self.inflow_l, self.inflow_h, 0], 
                [0, self.inflow_h, 0]
            ]),
        )
