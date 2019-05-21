from .baseproblem import *
from .tsolver import *

class TProblem(BaseProblem):
    defaults = {**BaseProblem.defaults, **dict(
        c   = 1.0,
        rho = 1.0,
        D   = 1.0,
        Q   = 0.0,
        T  = dict(
            title  = 'Temperature',
            rank   = Rank.scalar,
            family = Family.CG,
            degree = Degree.one,
        ),
        solver = TSolver,
    )}

    def neumann(self, F, v, T):
        for bounds, value in self.T.neumann:
            for i in bounds:
                F -= value*v*self.ds(i)
