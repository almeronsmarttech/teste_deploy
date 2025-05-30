class Pavimento:
    def __init__(self, nome = '', nivel = 0, fck=None, fyk=None, caa=None):
        self.nome = nome
        self.fck = fck
        self.fyk = fyk
        self.caa = caa
        self.nivel = nivel
        self.elementos = []

    def set_defaults_from_structure(self, estrutura):
        self.fck = self.fck or estrutura.fck
        self.fyk = self.fyk or estrutura.fyk
        self.caa = self.caa or estrutura.caa

    def add_element(self, element):
        element.set_context_from_floor(self)
        self.elementos.append(element)
