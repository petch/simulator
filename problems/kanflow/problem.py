from solver import *

class Problem(NSProblem):
    defaults = {**NSProblem.defaults, **dict(
        wall_u = (0.0, 0.0),
        inflow_u = ('0', '-sin(pi*(x[0]*x[0]*x[0]-3*x[0]*x[0]+3*x[0]))'),
        outflow_g = (0.0, 0.0),
        pa = 0.0,
    )}

    def conditions(self):
        self.u.dirichlet = [
            ([4], self.inflow_u, None),
            ([2, 5], self.wall_u, None),
        ]
        self.u.neumann = [
            ([3], self.outflow_g),
        ]
        self.p.integral = self.pa