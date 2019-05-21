from .common import *

class LinearSolver(Enum):
    default = 0
    mumps, petsc, superlu, umfpack = 1, 2, 3, 4
    bicgstab, cg, gmres, minres, richardson, tfqmr = 5, 6, 7, 8, 9, 10

class Preconditioner(Enum):
    default = 0
    none, icc, jacobi, ilu, sor = 1, 2, 3, 4, 5
    amg, hypre_amg, petsc_amg = 6, 7, 8
    hypre_euclid, hypre_parasails = 9, 10

class System(object):
    def __init__(self, problem, names):
        self.problem = problem
        self.names = names
        self.correction = None
        unknowns = problem.unknowns

        self.integrals = []
        self.elements = [unknowns[name].element for name in names]
        for name in names:
            if unknowns[name].integral is not None:
                self.integrals.append(name)
                self.elements.append(FiniteElement('Real', problem.mesh.ufl_cell(), 0))

        if len(names) == 1 and len(self.integrals) == 0:
            self.W = FunctionSpace(problem.mesh, self.elements[0])
        else:
            self.W = FunctionSpace(problem.mesh, MixedElement(self.elements))
        self.w = TrialFunction(self.W)
        self.z = TestFunction(self.W)
        self.w_ = Function(self.W)
        self.w0 = Function(self.W)

        if len(names) == 1 and len(self.integrals) == 0:
            self.spaces  = dict(zip(names, [self.W]))
            self.trials  = dict(zip(names, [self.w]))
            self.tests   = dict(zip(names, [self.z]))
            self.values  = dict(zip(names, [self.w_]))
            self.results = dict(zip(names, [self.w_]))
            self.lasts   = dict(zip(names, [self.w0]))
        else:
            self.spaces  = dict(zip(names, [self.W.sub(i) for i in range(len(names))]))
            self.trials  = dict(zip(names, list(split(self.w))[:len(names)]))
            self.tests   = dict(zip(names, list(split(self.z))[:len(names)]))
            self.values  = dict(zip(names, list(split(self.w_))[:len(names)]))
            self.results = dict(zip(names, list(self.w_.split())[:len(names)]))
            self.lasts   = dict(zip(names, list(split(self.w0))[:len(names)]))

        for k, v in self.results.items():
            v.rename(k, unknowns[k].title)
            unknowns[k].result = v

        self.bcs = []
        for name in names:
            self.bcs += problem.dirichlet(name, self.spaces[name])

        if not problem.stationary:
            initials = []
            for name in names:
                initials.append(problem.initial(name, self.spaces[name].collapse()))
            assign(self.w0, initials)
            assign(self.w_, self.w0)

    def functions(self, name):
        return self.trials[name], self.tests[name], self.values[name], self.lasts[name]

    def integral(self, F, nonlinear=False):
        c  = dict(zip(self.integrals, list(split(self.w))[len(self.integrals):]))
        r  = dict(zip(self.integrals, list(split(self.z))[len(self.integrals):]))
        c_ = dict(zip(self.integrals, list(split(self.w_))[len(self.integrals):]))
        if nonlinear:
            for name in self.integrals:
                F += (self.values[name] - self.problem.unknowns[name].integral)*r[name]*dx + c_[name]*self.tests[name]*dx
        else:
            for name in self.integrals:
                F += (self.trials[name] - self.problem.unknowns[name].integral)*r[name]*dx + c[name]*self.tests[name]*dx


class BaseSolver(object):
    defaults = dict(
        dmin = 1e-9,
        dmax = 1e+5,
        linear_solver = LinearSolver.default,
        preconditioner = Preconditioner.default,
    )

    def systems(self):
        raise NotImplementedError

    def __init__(self, problem, **params):
        self.problem = problem
        self.params = {**self.__class__.defaults,  **params}
        self.__dict__.update(self.params)
        self.solver_parameters = { 'linear_solver': self.linear_solver.name, 'preconditioner': self.preconditioner.name}

    def solve(self):
        problem = self.problem
        systems = self.systems()
        unknowns = problem.unknowns

        norms = dict(zip(unknowns.keys(), [open(f'{problem.path}/{name}.txt', 'w') for name in unknowns.keys()]))
        files = dict(zip(unknowns.keys(), [XDMFFile(f'{problem.path}/{name}.xdmf') for name in unknowns.keys()]))

        for k, v in unknowns.items():
            v.norm = norm(v.result)
            norms[k].write(f'{float(problem.t)}\t{v.norm}')
            files[k].write(v.result, float(problem.t))

        print([v.norm for k, v in unknowns.items()])

        while problem.next():
            for s in systems:
                solve(s.lhs == s.rhs, s.w_, s.bcs, solver_parameters=self.solver_parameters)
            for s in systems:
                if s.correction is not None:
                    solve(lhs(s.correction) == rhs(s.correction), s.w_, solver_parameters=self.solver_parameters)
            for s in systems:
                assign(s.w0, s.w_)

            for k, v in unknowns.items():
                v.norm = norm(v.result)
                norms[k].write(f'{float(problem.t)}\t{v.norm}')
                files[k].write(v.result, float(problem.t))

            print([v.norm for k, v in unknowns.items()])

        for k, v in unknowns.items():
            save_plot(problem.path, k, v.result)
            