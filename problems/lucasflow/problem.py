from solver import *

class Problem(NSProblem):
    defaults = {**NSProblem.defaults, **dict(
        ue = ('-cos(pi*x[0])/pi', '-x[1]*sin(pi*x[0])'),
        pe = '0',
        pa = 0.0,
    )}

    def conditions(self):
        self.f = self.source(self.ue, self.pe)
        self.u.dirichlet = [
            ([2, 3, 4, 5], self.ue, None),
        ]
        self.p.integral = self.pa

