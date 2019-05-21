from .common import *
from mpi4py import MPI
import sys
import pprint
import inspect

class Logger(object):
    def __init__(self, path, level):
        set_log_level(level)
        self.rank = MPI.COMM_WORLD.Get_rank()
        if (self.rank != 0):
            return
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.out = sys.stdout
        self.log = open(path, "w")
    def write(self, message):
        if (self.rank != 0):
            return
        self.out.write(message)
        self.log.write(message)
    def flush(self):
        if (self.rank != 0):
            return
        self.out.flush()
        self.log.flush()

class Simulation(object):
    def __init__(self, Domain, Problem, level=LogLevel.WARNING):
        self.Domain  = Domain
        self.Problem = Problem
        self.level   = level
        self.path    = f'{os.path.dirname(inspect.getfile(Problem))}/results/'

    def run(self, params, variants):
        p = {**self.Domain.defaults, **self.Problem.defaults, **params}
        self.vary(self.path, p, variants)

    def vary(self, path, params, variants):
        if len(variants) == 0:
            self.solve(path, params)
            return
        key, values = variants.popitem()
        p = params.copy()
        for i in range(len(values)):
            v = values[i]
            if isinstance(v, int) or isinstance(v, float) or isinstance(v, str):
                t = f'{v}'
            elif inspect.isclass(v):
                t = v.__name__
            else:
                t = f'{i}'
            p[key] = v
            self.vary(path + f'{key}{t}', p, variants)

    def solve(self, path, params):
        os.makedirs(path, exist_ok=True)
        open(f'{path}/params.txt', 'w').write(pprint.pformat(params))
        sys.stdout = Logger(f'{path}/!out.txt', self.level)

        domain = self.Domain(path, **params)
        domain.generate()
        problem = self.Problem(path, **params)
        problem.solve()
        
        sys.stdout = sys.__stdout__
