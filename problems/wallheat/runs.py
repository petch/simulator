from .domain import *
from .problem import *

simulation = Simulation(Domain, Problem)

simulation.run(
    dict(),
    dict(cellscale = [2.0, 1.0, 0.5, 0.25])
)
