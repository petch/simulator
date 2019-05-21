from .domain import *
from .problem import *

simulation = Simulation(Domain, Problem)
print(lu_solver_methods())

simulation.run(
    dict(solver_type=NSSolverType.duoglas),
    dict(cellscale = [1.0, 0.5, 0.25, 0.125])
)