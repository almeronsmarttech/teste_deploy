import numpy as np

class Aco:
    def __init__(self, fyk=500, gama_s = 1.15):
        self.__gama_s = gama_s
        self.__fyk = fyk
        self.__fyd = self.__fyk/10/self.__gama_s # kN/cm2
        self.__es = 21000
        print(f"Aço\nfyk: {self.__fyk} MPa\t fyd: {self.__fyd:.4f} kN/cm2\t Es: {int(self.__es)} MPa")

    @property
    def fyd(self):
        return self.__fyd


class Barra:

    def __init__(self, aco:Aco, diametro=5.0, comprimento = 1200):
        self.__aco = aco
        self.__diametro = diametro / 10 # em cm
        self.__comprimento = comprimento

    def __str__(self):
        return f"diâmetro:{self.diametro}\tárea de aço:{self.area_aco}\tperímetro:{self.perimetro}"

    @property
    def diametro(self):
        return self.__diametro

    @property
    def area_aco(self):
         return  np.pi * (self.__diametro/2)**2

    @property
    def perimetro(self):
        return np.pi * self.__diametro

    def massa_linear(self):
        return self.area_aco() * 7.8 * 1
