from ..enums import TipoAgregado
import numpy as np


class Madeira:

    def __init__(self, D=20, u_amb=65, kmod1=1, gama_w_c=1.4, gama_w_t=1.4, gama_w_v=1.8):
        # coficientes ponderadores
        self.__gama_w_c = gama_w_c
        self.__gama_w_t = gama_w_t
        self.__gama_w_v = gama_w_v
        #gama_F = 1.4

        self.__u_amb = u_amb
        #self.__carregamento = carregamento
        #self.__kmod1 = 1.0
        self.__kmod1 = kmod1
        #self.__kmod2 = 1.0

        if D == 20:
            self.__fc0k = 20
            self.__fv0k = 4
            self.__Ec0med = 10000
            self.__ro_a_12 = 500
        elif D == 30:
            self.__fc0k = 30
            self.__fv0k = 5
            self.__Ec0med = 12000
            self.__ro_a_12 = 625
        elif D == 40:
            self.__fc0k = 40
            self.__fv0k = 6
            self.__Ec0med = 14500
            self.__ro_a_12 = 750
        elif D == 50:
            self.__fc0k = 50
            self.__fv0k = 7
            self.__Ec0med = 16500
            self.__ro_a_12 = 850
        elif D == 60:
            self.__fc0k = 60
            self.__fv0k = 8
            self.__Ec0med = 19500
            self.__ro_a_12 = 1000

        print("Caracterização do material")
        #
        # if self.__carregamento == 1:
        #     self.__kmod1 = 0.6
        # if self.__carregamento == 2:
        #     self.__kmod1 = 0.7
        # if self.__carregamento == 3:
        #     self.__kmod1 = 0.8
        # if self.__carregamento == 4:
        #     self.__kmod1 = 0.9
        # if self.__carregamento == 5:
        #     self.__kmod1 = 1.1

        if self.__u_amb <= 65:
            self.__u_eq = 12  # classe de umidade 1
            self.__kmod2 = 1.0
        elif self.__u_amb <= 75:
            self.__u_eq = 15  # classe de umidade 2
            self.__kmod2 = 0.9
        elif self.__u_amb <= 85:
            self.__u_eq = 18  # classe de umidade 3
            self.__kmod2 = 0.8
        else:
            self.__u_eq = 25  # classe de umidade III
            # ou mais
            self.__kmod2 = 0.7

        self.__kmod = self.__kmod1 * self.__kmod2
        # Valor fc0k Corrigido para a umidade ambiente
        self.__fu = self.__fc0k / (1 + (3 * (self.__u_eq - 12)) / 100)
        self.__fc0k = self.__fu
        self.__fc0k /= 10
        self.__fmk = self.__fc0k
        self.__Ec0med /= 10 # MPa para kN/cm2
        self.__ro_a_12 /= 100  # kgf para (kN/m3) massa específica aparente -tabelado
        # Valor Módulo Corrigido para a umidade ambiente
        self.__Eu = self.__Ec0med / (1 + (2 * (self.__u_eq - 12)) / 100)
        self.__E0ef = self.__Eu * self.__kmod  # E c0 efetivo
        self.__E0_05 = 0.7 * self.__E0ef
        self.__fc0d = (self.__kmod * self.__fc0k) / self.__gama_w_c
        self.__fmd = (self.__kmod * self.__fc0k) / self.__gama_w_t
        self.__ft0d = (self.__kmod * self.__fc0k) / (self.__gama_w_t * 0.77)
        self.__fv0k /= 10  # de MPa para kN/cm2
        self.__fuv = self.__fv0k / (1 + (3 * (self.__u_eq - 12)) / 100)
        self.__fv0k = self.__fuv
        self.__fv0d = self.__fuv/ self.__gama_w_c

        self.__fv90d = (self.__kmod * self.__fuv) / self.__gama_w_v

        print(f"Madeira\nkmod1: {self.__kmod1}\t kmod2: {self.__kmod2}\t kmod: {self.__kmod}")
        print(f"Madeira\nfc0k: {self.__fc0k} MPa\t fmk: {round(self.__fmk,2)}\t E0_05: {round(self.__E0_05,2)}")
        print(f"fcd: {self.__fc0d:.2f} kN/cm2\tfmd: {self.__fmd:.2f} kN/cm2\tft0d: {self.__ft0d:.2f} kN/cm2\tfv0d: {self.__fv0d:.2f} kN")

    @property
    def u_eq(self):
        return self.__u_eq

    @property
    def Ec0med(self):
        return self.__Ec0med

    @property
    def E0_05(self):
        return self.__E0_05

    @property
    def E0ef(self):
        return self.__E0ef

    @property
    def nu(self):
        return self.__nu

    @property
    def fc0k(self):
        return self.__fc0k

    @property
    def fc0d(self):
        return self.__fc0d

    @property
    def ft0d(self):
        return self.__ft0d

    @property
    def fv0d(self):
        return self.__fv0d

    @property
    def fmd(self):
        return self.__fmd

    @property
    def kmod(self):
        return self.__kmod


