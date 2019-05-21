from .basesolver import *

class TSolver(BaseSolver):
    def systems(self):
        problem = self.problem
        dt, c, rho, D, Q = problem.dt, problem.c, problem.rho, problem.D, problem.Q
        s = System(problem, ['T'])
        T, v, T_, T0 = s.functions('T')

        F = c*rho/dt*(T - T0)*v*dx \
          + inner(D*grad(T), grad(v))*dx \
          - Q*v*dx
        problem.neumann(F, v, T)
        s.integral(F)

        s.lhs, s.rhs = lhs(F), rhs(F)
        return [s]
