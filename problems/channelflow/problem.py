from solver import *

class Problem(NSProblem):
    defaults = {**NSProblem.defaults, **dict(
        f         = (0.0, 0.0),
        h         = 0.2,
        wall_u    = (0.0, 0.0),
        bottom_u  = 0.0,
        outflow_g = (0.0, 0.0),
        outflow_p = 0.0,
        inflow_u  = ('(h-x[1])*(h+x[1])/h/h', '0'),
        pa        = 0.0,
    )}

    def conditions(self):
        self.u.dirichlet = [
            ([4, 5, 6], self.wall_u, None),
            ([7], self.inflow_u, None),
            ([2], self.bottom_u, 1),
        ]
        self.u.neumann = [
            ([3], self.outflow_g)
        ]
        self.p.dirichlet = [
            ([3], self.outflow_p, None)
        ]
        # self.p.integral = self.pa
