class Propellant:

    def __init__(self, name, density):
        self.name = name
        self.density = density


class Material:

    def __init__(self, name, density, tensile_strength):
        self.name = name
        self.density = density
        self.tensile_strength = tensile_strength
