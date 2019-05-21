from .baseproblem import *
from .nssolver import *

class Convection(Enum):
    divergence    = 0
    advective     = 1
    skewsymmetric = 2
    rotation      = 3

class NSProblem(BaseProblem):
    defaults = {**BaseProblem.defaults, **dict(
        convection = Convection.divergence,
        rho = 1.0,
        mu  = 1.0,
        pa  = 0.0,
        f   = ('0', '0'),
        u   = dict(
            title  = 'Velocity',
            rank   = Rank.vector,
            family = Family.CG,
            degree = Degree.two,
        ),
        p   = dict(
            title  = 'Pressure',
            rank   = Rank.scalar,
            family = Family.CG,
            degree = Degree.one,
        ),
        solver = NSSolver,
    )}

    def __init__(self, path='results/default', **params):
        super(NSProblem, self).__init__(path, **params)
        self.convection = getattr(self, self.convection.name)

    def divergence(self, u1, u2):
        return div(outer(u1, u2))

    def advective(self, u1, u2):
        return dot(u1, nabla_grad(u2))

    def skewsymmetric(self, u1, u2):
        return 0.5*self.divergence(u1, u2) + 0.5*self.advective(u1, u2)

    def rotation(self, u1, u2):
        return curl(u2)*as_vector((-u1[1], u1[0])) + 0.5*nabla_grad(dot(u1, u2))

    def stress(self, u, p):
        return 2*self.mu*sym(nabla_grad(u)) - p*Identity(len(u))

    def neumann_stress(self, F, v, u, p):
        sn = dot(self.mu*nabla_grad(u) - p*Identity(len(u)), self.n)
        # F -= dot(sn, v)*self.ds
        for bounds, value in self.u.neumann:
            for i in bounds:
                F -= dot(self.mu*value + sn, v)*self.ds(i)

    def source(self, u, p):
        return self.rho*self.convection(u, u) - div(self.stress(u, p))
