from .common import *

class Family(Enum):
    CG = 0
    DG = 1

class Degree(Enum):
    zero  = 0
    one   = 1
    two   = 2
    three = 3

class Rank(Enum):
    scalar = 0
    vector = 1
    tensor = 2

class Unknown(object):
    def __init__(self, name, params, cell):
        self.name = name
        self.__dict__.update(params)
        
        if self.rank == Rank.scalar:
            self.element = FiniteElement(self.family.name, cell, self.degree.value)
        if self.rank == Rank.vector:
            self.element = VectorElement(self.family.name, cell, self.degree.value)
        if self.rank == Rank.tensor:
            self.element = TensorElement(self.family.name, cell, self.degree.value)
        
        self.initial   = None
        self.integral  = None
        self.dirichlet = []
        self.neumann   = []
        self.robin     = []

class BaseProblem(object):
    defaults = dict(
        stationary = True,
        t  = 0.0,
        te = 10.0,
        dt = 1.0,
        solver = None,
    )

    def conditions(self):
        raise NotImplementedError

    def solve(self):
        raise NotImplementedError

    def __init__(self, path='results/default', **params):
        self.path = path
        self.params = {**self.__class__.defaults,  **params}
        self.__dict__.update(self.params)

        self.mesh = Mesh(f'{self.path}/mesh.xml')
        self.subdomains = MeshFunction('size_t', self.mesh, f'{self.path}/subdomains.xml') 
        self.boundaries = MeshFunction('size_t', self.mesh, f'{self.path}/boundaries.xml') 

        self.dx = Measure('dx', domain=self.mesh, subdomain_data=self.subdomains)
        self.ds = Measure('ds', domain=self.mesh, subdomain_data=self.boundaries)
        self.n  = FacetNormal(self.mesh)

        self.unknowns = dict()
        for k, v in self.params.items():
            if isinstance(v, dict):
                self.unknowns[k] = Unknown(k, v, self.mesh.ufl_cell())
        self.__dict__.update(self.unknowns)

        self.constants = dict()
        for k, v in self.params.items():
            if isinstance(v, float) or isinstance(v, tuple) and isinstance(v[0], float):
                self.constants[k] = Constant(v)
            if isinstance(v, list) and isinstance(v[0], float):
                self.constants[k] = Coefficient(self.subdomains, v)
        self.__dict__.update(self.constants)

        self.expressions = dict()
        for k, v in self.params.items():
            if isinstance(v, str) or isinstance(v, tuple) and isinstance(v[0], str):
                self.expressions[k] = Expression(v, degree=2, domain=self.mesh, **self.constants)
        self.__dict__.update(self.expressions)

    def initial(self, name, space):
        return project(self.unknowns[name].initial, space)

    def dirichlet(self, name, space):
        bcs = []
        for bounds, value, index in self.unknowns[name].dirichlet:
            if index is not None:
                space = space.sub(index)
            for i in bounds:
                bcs.append(DirichletBC(space, value, self.boundaries, i))
        return bcs

    def solve(self):
        self.conditions()
        self.solver(self, **self.params).solve()
        
    def next(self):
        self.t.assign(float(self.t) + float(self.dt))
        return float(self.t) < float(self.te) + float(self.dt)/2