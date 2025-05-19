from ..materials.concreto import Concreto
from ..materials.aco import Aco
from ..codes.nbr_6118_2023 import cobrimento

class Estrutura:
    def __init__(self, nome = '', norma = "nbr_6118_2023", concreto = Concreto(fck=25), aco = Aco(fyk=500), caa="III", gama_c=1.4, gama_s=1.15, gama_F=1.4):
        self.nome = nome
        self.concreto = concreto
        self.aco = aco
        self.norma = norma
        self.caa = caa
        self.gama_c = gama_c
        self.gama_s = gama_s
        self.gama_F = gama_F
        self.pavimentos = []

    def cobrimento_nominal(self, tipo_elemento: str) -> int:
        if self.norma == "nbr_6118_2023":
            return cobrimento.cobrimento_nbr6118(tipo_elemento, self.caa)
        else:
            raise NotImplementedError(f"Norma '{self.norma}' ainda não implementada para cobrimento.")

    def adicionar_pavimento(self, pavimento):
        pavimento.set_defaults_from_structure(self)
        self.pavimentos.append(pavimento)