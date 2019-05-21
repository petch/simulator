from .domain import *

class Problem(NSProblem):
    defaults = {**NSProblem.defaults, **dict(
        ue = ('(1+mu*t)*2*x[0]*x[0]*(x[0]-1)*(x[0]-1)*x[1]*(2*x[1]-1)*(x[1]-1)', '-(1+mu*t)*2*x[0]*(2*x[0]-1)*(x[0]-1)*x[1]*x[1]*(x[1]-1)*(x[1]-1)'),
        pe = 'rho*x[1]',
        pa = 'rho*0.5',
    )}

    def conditions(self):
        self.f = self.source(self.ue, self.pe)
        self.u.dirichlet = [
            ([2, 3, 4, 5], self.ue, None),
        ]
        self.p.integral = self.pa
