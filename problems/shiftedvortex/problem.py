from solver import *

class Problem(NSProblem):
    defaults = {**NSProblem.defaults, **dict(
        mu = 0.01,
        ue = ('40*2*exp(x[0])*pow(x[0]-1,2)*pow(x[0],2)*x[1]*(x[1]-1)*(2*x[1]-1)', '-40*exp(x[0])*(x[0]-1)*x[0]*(x[0]*(3+x[0])-2)*pow(x[1]-1,2)*pow(x[1],2)'),
        pe = '10*(-424+156*exp(1)+(x[1]*x[1]-x[1])*(-456+exp(x[0])*(456+pow(x[0],2)*(228-5*(x[1]*x[1]-x[1]))+2*x[0]*(-228+(x[1]*x[1]-x[1]))+2*pow(x[0],3)*(-36+(x[1]*x[1]-x[1]))+pow(x[0],4)*(12+(x[1]*x[1]-x[1])))))',
        pa = 0.0,
    )}

    def conditions(self):
        self.f = self.source(self.ue, self.pe)
        self.u.dirichlet = [
            ([2, 3, 4, 5], self.ue, None),
        ]
        self.p.integral = self.pa
