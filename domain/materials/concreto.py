from enum import Enum

import numpy as np

class TipoAgregado(Enum):
    BASALTO_DIABASIO = 1.2
    GRANITO_GNAISSE = 1.0
    CALCARIO = 0.9
    ARENITO = 0.7

class Concreto:

    def __init__(self, fck=20, tipo_agregado: TipoAgregado = TipoAgregado.ARENITO, gama_c = 1.4, nu = 0.2):
        self.__gama_c = gama_c
        self.__nu = nu
        self.__fck = fck

        self.__fcd = self.__fck/10/self.__gama_c # kN/cm2
        self.__fctk_m = 0.3 * np.pow(self.__fck, 2/3) / 10  # em kN/cm2
        self.__fctk_sup = 1.3 * self.__fctk_m  # em kN/cm2
        self.__fctk_inf = 0.7 * self.__fctk_m  # em kN/cm2
        # print(f"fck :{self.__fck}\tfct_m :{self.__fctk_m} fctk_sup: {self.__fctk_sup}")
        self.__alfa_e = tipo_agregado.value
        self.__eci = self.calcular_Eci() # kN/cm2
        self.__alfa_i = min(0.8 + 0.2 * self.__fck/80,1)
        self.__ecs = self.__alfa_i * self.__eci
        print(f"Concreto\nfck: {self.__fck} MPa\t alfai: {round(self.__alfa_i,3)}\t Eci: {int(self.__eci)} MPa\t Ecs: {int(self.__ecs)} MPa")
        print(f"fcd: {self.__fcd:.4f} kN/cm2\tfctk m: {self.__fctk_m:.4f} kN/cm2\tfctk sup: {self.__fctk_sup:.4f} kN/cm2\tfctk inf: {self.__fctk_inf:.4f} kN/cm2")

    def calcular_Eci(self):
        if self.__fck <= 50:
            Eci = self.__alfa_e * 5600 * (self.__fck ** 0.5)
        else:
            Eci = 21500 * self.__alfa_e * ((self.__fck / 10 + 1.25) ** (1/3))
        return int(Eci)

    @property
    def Ecs(self):
        return self.__ecs

    @property
    def nu(self):
        return self.__nu

    @property
    def fck(self):
        return self.__fck

    @property
    def fcd(self):
        return self.__fcd

    @property
    def fctk_sup(self):
        return self.__fctk_sup