from solver import *

class Problem(TProblem):
    defaults = {**TProblem.defaults, **dict(
        c   = [0.0, 1.0, 1.0],
        rho = [0.0, 80.0, 10.0],
        D   = [0.0, 1.0, 0.1],
        T_inside  = 100.0,
        T_outside = 0.0,
        T_initial = 0.0,
    )}

    def conditions(self):
        self.T.dirichlet = [
            ([6], self.T_inside, None),
            ([8], self.T_outside, None),
        ]
        self.T.initial = self.T_initial