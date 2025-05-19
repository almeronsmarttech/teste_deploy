from domain.structure.estrutura import Estrutura
from domain.codes.nbr_6118_2023.flexao import dimensionar_flexao_secao_retangular
from domain.codes.nbr_6118_2023.cisalhamento import dimensionar_cisalhamento_secao_retangular
from domain.codes.nbr_6118_2023.armadura_minima import ro_min, row_min

class Viga:
    def __init__(self, bw: int, h: int, estrutura = Estrutura()):
        self._bw = bw
        self._h = h
        self._estrutura = estrutura
        self.cobrimento = self.cobrimento()
        self._d = self._h - 5
        self._concreto = estrutura.concreto
        self.__aco = estrutura.aco

        self._D = (self._concreto.Ecs * self._h / 10 * self._h / 10 * self._h / 10) / (12 * (1 - (self._concreto.nu * self._concreto.nu))) #  rigidez
        print(f"D: {int(self._D)} kN")
        self.__W0 = self._bw * self._h * self._h / 6  # módulo resistente cm3
        print(f"W0: {self.__W0:.2f} cm3")
        #self._w0 = 0 # flecha inicial m
        #self.__wf = 0  # flecha inicial m
        #self._wlim = min(self._lx, self._ly) / 250
        #self.__alfa_f = 0 #coeficiente multiplicador de flechas para consideração de fluência (cargas de longa duração)
        self.__Mdmin = 0.8 * self.__W0 * self._concreto.fctk_sup
        #print(f"Md_min: {self.__Mdmin:.2f} kN.cm/m")

        print(f"ro_min: {ro_min(estrutura.concreto.fck)}")
        print(f"row_min: {row_min(estrutura.concreto.fck)}")
        #self._As_min = max(self.__ro_min * self.__b * self.__h,self.calcular_As(self.__Mdmin))
        #self._As_min = self.calcular_As(self.__Mdmin/100)
        self._As_min = ro_min(estrutura.concreto.fck) * self._bw * self._h
        self._Asw_min = row_min(estrutura.concreto.fck) * self._bw * 100

        #self.__bitolas = bitolas
        self.__bitolas_possiveis = []
        self.__espacamento_minimo = 8.0
        self.__espacamento_maximo = min(20.0, self._h * 2)


    def cobrimento(self):
        return self._estrutura.cobrimento_nominal("viga")

    def calcular_As(self, momento):
        return dimensionar_flexao_secao_retangular(self._bw,self._h,momento, self._estrutura)

    def calcular_Asw(self, cortante):
        return dimensionar_cisalhamento_secao_retangular(self._bw,self._h,cortante, self._estrutura)