from .domain import *
from .problem import *

simulation = Simulation(Domain, Problem)

simulation.run(
    dict(linear_solver=LinearSolver.umfpack),
    dict(cellscale = [1.0, 0.5, 0.25, 0.125])
)
