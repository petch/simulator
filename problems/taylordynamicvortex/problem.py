from solver import *

class Problem(NSProblem):
    defaults = {**NSProblem.defaults, **dict(
        mu = 0.01,
        ue = ('-cos(pi*x[0])*sin(pi*x[1])*exp(-2*pi*pi*mu*t)', 'sin(pi*x[0])*cos(pi*x[1])*exp(-2*pi*pi*mu*t)'),
        pe = '-0.25*rho*(cos(2*pi*x[0])+cos(2*pi*x[1]))*exp(-4*pi*pi*mu*t)',
        pa = 0.0,
    )}

    def conditions(self):
        self.f = self.source(self.ue, self.pe)
        self.u.dirichlet = [
            ([2, 3, 4, 5], self.ue),
        ]
        self.p.integral = self.pa
