import numpy as np
from numpy.ma.core import floor

from domain.structure.estrutura import Estrutura
from domain.codes.nbr_6118_2023.flexao_simples_araujo import dimensionar_flexao_secao_retangular
from domain.codes.nbr_6118_2023.flexao_simples_faccio import flexao_simples_retangular
from domain.codes.nbr_6118_2023.cisalhamento import dimensionar_cisalhamento_secao_retangular
from domain.codes.nbr_6118_2023.armadura_minima import ro_min, row_min

class VigaRetangular:
    def __init__(self, bw: int, h: int, estrutura = Estrutura()):
        self._bw = bw
        self._h = h
        self._estrutura = estrutura
        self.cobrimento = self.cobrimento()
        #self._d = self._h - self.cobrimento - self._estrutura.diametro_estribo_viga - self._estrutura.diametro_logitudinal_viga / 2
        self._dl = 4
        self._d = self._h - self._dl
        self._concreto = estrutura.concreto
        self._aco = estrutura.aco

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
        self._as_min = ro_min(estrutura.concreto.fck) * self._bw * self._h
        self._asw_min = row_min(estrutura.concreto.fck) * self._bw * 100
        #self._as = 0
        self._as1, self._as2 = 0,0 # Armadura de tração e Armadura de compressão
        self._asw = 0
        self._as1_necessario = max(self._as_min, self._as1)
        self._as2_necessario = max(self._as_min, self._as2)
        self._asw_necessario = max(self._asw_min, self._asw)
        #self.__bitolas = bitolas
        #self.__bitolas_possiveis = []
        self.__espacamento_minimo = 5.0
        self.__espacamento_maximo = 20.0

    def cobrimento(self):
        return self._estrutura.cobrimento_nominal("viga")

    def calcular_As(self, momento):
        self._as1, self._as2 =dimensionar_flexao_secao_retangular(self, momento, self._estrutura)
        #if self._as is
        print(f"As tração: {self._as1} cm2\tAs compressão: {self._as2} cm2")
        flexao_simples_retangular(self, momento*self._estrutura.gama_F)

        # if isinstance(self._as, float):
        #     self._as_necessario = max(self._as_min, self._as)
        # else:
        #     self._as_necessario = 'Armadura Dupla'
        return self._as1, self._as2

    def detalhar_As(self, cobertura = 1, tamanho = 1):
        lista_resposta = []
        print("Entrou no método detalhar As")
        if (self._as1 > 0):
            for bitola in self._estrutura.bitolas_longitudinal:
                num_barras = np.ceil(self._as1_necessario / bitola.area_aco)
                print(f"num_barras: {num_barras}")

                print(f"{num_barras} Φ de {bitola.diametro * 10:.1f} mm.\tAs efetivo: {num_barras * bitola.area_aco:.2f} cm2.")
                lista_resposta.append(
                    f"{num_barras} Φ de {bitola.diametro * 10:.1f} mm. (As efetivo: {num_barras * bitola.area_aco:.2f} cm2/m)")
        return lista_resposta

    def detalhar_As_compressao(self, cobertura = 1, tamanho = 1):
        lista_resposta = []
        print("Entrou no método detalhar As'")
        if(self._as2 > 0):
            for bitola in self._estrutura.bitolas_longitudinal:
                num_barras = np.ceil(self._as2_necessario / bitola.area_aco)
                print(f"num_barras: {num_barras}")
                print(
                    f"{num_barras} Φ de {bitola.diametro * 10:.1f} mm.\tAs efetivo: {num_barras * bitola.area_aco:.2f} cm2.")
                lista_resposta.append(
                    f"{num_barras} Φ de {bitola.diametro * 10:.1f} mm. (As efetivo: {num_barras * bitola.area_aco:.2f} cm2/m)")
        return lista_resposta

    def calcular_Asw(self, cortante):
        self._asw = dimensionar_cisalhamento_secao_retangular(self._bw, self._d, cortante, self._estrutura)
        self._as_necessario = max(self._asw_min, self._asw)
        return self._as_necessario

    def detalhar_Asw(self, cobertura = 1, tamanho = 1, numero_ramos = 2):
        lista_resposta = []
        #for bitola in self._estrutura.bitolas_transversal:
        #    if self.__bitola_minima <= bitola.diametro <= self.__bitola_maxima:
        #        self.__bitolas_possiveis.append(bitola)
        print("Entrou no método detalhar Asw")
        for bitola in self._estrutura.bitolas_transversal:
            num_barras = self._asw_necessario / (bitola.area_aco * numero_ramos)
            espacamento = int(np.floor(100 / num_barras))
            print(f"{num_barras} Φ de {bitola.diametro * 10:.1f} mm a cada {espacamento} cm.\tAs efetivo: {num_barras / cobertura * bitola.area_aco:.2f} cm2/m.")
            if espacamento > self.__espacamento_maximo:
                espacamento = self.__espacamento_maximo
                # recalcula número de barras
                num_barras = 100 / espacamento
            if espacamento > self.__espacamento_minimo:
                num_barras = int(np.ceil(num_barras * cobertura))
                print(
                    f"{num_barras} Φ de {bitola.diametro * 10:.1f} mm a cada {espacamento} cm.\tAs efetivo: {num_barras / cobertura * bitola.area_aco*numero_ramos:.2f} cm2/m.")
                lista_resposta.append(
                    f"Φ de {bitola.diametro * 10:.1f} mm a cada {espacamento} cm. (As efetivo: {num_barras / cobertura * bitola.area_aco*numero_ramos:.2f} cm2/m)")
        return lista_resposta