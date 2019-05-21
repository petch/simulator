from dolfin import *
from enum import Enum
import matplotlib.pyplot as plt
import subprocess
import pygmsh
import inspect
import os

class Dimension(Enum):
    two = 2
    three = 3

def execute(command):
    print(f"Running: {command}")
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        line = process.stdout.readline()
        if not line:
            break
        print(line.decode("utf-8"), end="")
    process.communicate()
    print(f"Exited with code {process.returncode}.")

def save_plot(path, name, u, colorbar=True):
    plt.figure(name)
    if colorbar:
        plt.colorbar(plot(u))
    else:
        plot(u)
    plt.savefig(f'{path}/{name}.png', bbox_inches='tight')
    plt.clf()

def Coefficient(subdomains, values):
    code = """
    #include <pybind11/pybind11.h>
    namespace py = pybind11;
    #include <dolfin/common/Array.h>
    #include <dolfin/function/Expression.h>
    #include <dolfin/function/Constant.h>
    #include <dolfin/mesh/MeshFunction.h>
    class Coefficient : public dolfin::Expression {
    public:
        void eval(dolfin::Array<double> &v, const dolfin::Array<double> &x, const ufc::cell &cell) const override {
            v[0] = (*values).values()[int((*subdomains)[cell.index])];
        }
        std::shared_ptr<dolfin::MeshFunction<size_t>> subdomains;
        std::shared_ptr<dolfin::Constant> values;
    };
    PYBIND11_MODULE(SIGNATURE, m) {
    py::class_<Coefficient, std::shared_ptr<Coefficient>, dolfin::Expression>
        (m, "Coefficient")
        .def(py::init<>())
        .def_readwrite("subdomains", &Coefficient::subdomains)
        .def_readwrite("values", &Coefficient::values);
    }
    """
    return CompiledExpression(compile_cpp_code(code).Coefficient(), subdomains=subdomains, values=Constant(values), degree=0)