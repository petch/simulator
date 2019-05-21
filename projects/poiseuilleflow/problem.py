from solver import *

class Problem(NSProblem):
    defaults = {**NSProblem.defaults, **dict(
        ue = ('0.5/mu*x[1]*(1-x[1])', '0'),
        pe = '1.0-x[0]',
        wall_u = (0.0, 0.0),
        inflow_p = 1.0,
        inflow_u = (0.0, 0.0),
        outflow_p = 0.0,
        outflow_u = (0.0, 0.0),
    )}

    def conditions(self):
        self.f = self.source(self.ue, self.pe)
        self.u.dirichlet = [
            ([2, 4], self.wall_u, None),
        ]
        self.p.dirichlet = [
            ([5], self.inflow_p, None),
            ([3], self.outflow_p, None),
        ]
        self.u.neumann = [
            ([5], self.inflow_u),
            ([3], self.outflow_u),
        ]
