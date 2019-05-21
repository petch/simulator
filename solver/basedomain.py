from .common import *

class BaseDomain(object):
    defaults = dict(
        dim       = Dimension.two,
        cellscale = 1.0,
    )

    def geometry(self):
        raise NotImplementedError

    def __init__(self, path='results/default', **params):
        self.path = path
        self.params = {**self.__class__.defaults, **params}
        self.__dict__.update(self.params)

    def generate(self):
        # self.geom = pygmsh.opencascade.Geometry()
        self.geom = pygmsh.built_in.Geometry()
        self.shapes = []
        self.geometry() 

        self.geom.add_raw_code('Coherence;')

        for shape in self.shapes:
            if hasattr(shape, 'surface'):
                self.geom.add_physical(shape.surface)
            elif hasattr(shape, 'plane_surface'):
                self.geom.add_physical(shape.plane_surface)
        for shape in self.shapes:
            if hasattr(shape, 'lines'):
                for l in shape.lines:
                    self.geom.add_physical(l)

        os.makedirs(self.path, exist_ok=True)
        open(f'{self.path}/domain.geo', 'w').write(self.geom.get_code())
        execute(f"gmsh -{self.dim.value} -clscale {self.cellscale} -o {self.path}/mesh.msh {self.path}/domain.geo")
        execute(f"dolfin-convert {self.path}/mesh.msh {self.path}/mesh.xml")
        os.rename(f"{self.path}/mesh_physical_region.xml", f"{self.path}/subdomains.xml")
        os.rename(f"{self.path}/mesh_facet_region.xml", f"{self.path}/boundaries.xml")

        self.mesh       = Mesh(f'{self.path}/mesh.xml')
        self.subdomains = MeshFunction('size_t', self.mesh, f'{self.path}/subdomains.xml')
        self.boundaries = MeshFunction('size_t', self.mesh, f'{self.path}/boundaries.xml')

        XDMFFile(f'{self.path}/mesh.xdmf').write(self.mesh)
        XDMFFile(f'{self.path}/subdomains.xdmf').write(self.subdomains)
        XDMFFile(f'{self.path}/boundaries.xdmf').write(self.boundaries)

        save_plot(self.path, 'mesh', self.mesh, False)
        save_plot(self.path, 'subdomains', self.subdomains, False)
