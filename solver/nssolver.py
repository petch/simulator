from .basesolver import *

class NSSolverType(Enum):
    nonlinear = 0
    linear    = 1
    ipcs      = 2
    duoglas   = 3

class NSSolver(BaseSolver):
    defaults = {**BaseSolver.defaults, **dict(
        solver_type = NSSolverType.nonlinear,
    )}

    def __init__(self, problem, **params):
        super(NSSolver, self).__init__(problem, **params)
        self.systems = getattr(self, self.solver_type.name)
        if self.solver_type == NSSolverType.nonlinear:
            self.solver_parameters = {'newton_solver': self.solver_parameters}

    def nonlinear(self):
        problem = self.problem
        dt, rho, mu, f = problem.dt, problem.rho, problem.mu, problem.f
        s = System(problem, ['u', 'p'])
        u, v, u_, u0 = s.functions('u')
        p, q, p_, p0 = s.functions('p')

        F = rho*dot(problem.convection(u_, u_), v)*dx \
          + inner(problem.stress(u_, p_), sym(nabla_grad(v)))*dx \
          - dot(f, v)*dx \
          + dot(div(u_), q)*dx
        problem.neumann_stress(F, v, u_, p_)
        s.integral(F, True)

        if not problem.stationary:
            F += rho/dt*dot(u_ - u0, v)*dx

        s.lhs, s.rhs = F, 0
        return [s]

    def linear(self):
        problem = self.problem
        rho, dt, mu, f, n, ds = problem.rho, problem.dt, problem.mu, problem.f, problem.n, problem.ds
        s = System(problem, ['u', 'p'])
        u, v, u_, u0 = s.functions('u')
        p, q, p_, p0 = s.functions('p')

        F = rho/dt*dot(u - u0, v)*dx \
          + rho*dot(problem.convection(u, u0), v)*dx \
          + inner(problem.stress(u, p), sym(nabla_grad(v)))*dx \
          - dot(f, v)*dx \
          + dot(div(u), q)*dx
        problem.neumann_stress(F, v, u, p)
        s.integral(F, False)

        s.lhs, s.rhs = lhs(F), rhs(F)
        return [s]
        
    def ipcs(self):
        problem = self.problem
        rho, dt, mu, f = problem.rho, problem.dt, problem.mu, problem.f
        su = System(problem, ['u'])
        u, v, u_, u0 = su.functions('u')
        sp = System(problem, ['p'])
        p, q, p_, p0 = sp.functions('p')
        U = (u + u0)/2

        Fu = rho/dt*dot(u - u0, v)*dx \
           + rho*dot(problem.convection(u0, u0), v)*dx \
           + inner(problem.stress(U, p0), sym(nabla_grad(v)))*dx \
           - dot(f, v)*dx
        problem.neumann_stress(Fu, v, U, p0)
        su.integral(Fu)
        su.lhs, su.rhs = lhs(Fu), rhs(Fu)

        Fp = dot(nabla_grad(p - p0), nabla_grad(q))*dx + rho/dt*div(u_)*q*dx
        sp.integral(Fp)
        sp.lhs, sp.rhs = lhs(Fp), rhs(Fp)
        
        su.correction = dot(u - u_, v)*dx + dt/rho*dot(nabla_grad(p_ - p0), v)*dx

        return [su, sp]

    def duoglas(self):
        problem = self.problem
        rho, dt, mu, f = problem.rho, problem.dt, problem.mu, problem.f
        su = System(problem, ['u'])
        u, v, u_, u0 = su.functions('u')
        sp = System(problem, ['p'])
        p, q, p_, p0 = sp.functions('p')

        Fu = rho/dt*dot(u - u0, v)*dx \
           + rho*dot(problem.convection(u0, u), v)*dx \
           + inner(problem.stress(u, p0), sym(nabla_grad(v)))*dx \
           - dot(f, v)*dx
        problem.neumann_stress(Fu, v, u, p0)
        su.integral(Fu)
        su.lhs, su.rhs = lhs(Fu), rhs(Fu)

        Fp = dot(nabla_grad(p - p0), nabla_grad(q))*dx + rho/dt*div(u_)*q*dx
        sp.integral(Fp)
        sp.lhs, sp.rhs = lhs(Fp), rhs(Fp)

        su.correction = dot(u - u_, v)*dx + dt/rho*dot(nabla_grad(p_ - p0), v)*dx

        return [su, sp]
