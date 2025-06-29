from ..enums import TipoAgregado
import numpy as np


class Concreto:

    def __init__(self, fck=20, tipo_agregado: TipoAgregado = TipoAgregado.ARENITO, gama_c=1.4, nu=0.2):
        self.__gama_c = gama_c
        self.__nu = nu
        self.__fck = int(fck)
        self.__fcd = self.__fck / 10 / self.__gama_c  # kN/cm2
        self.__fctk = 0.3 * self.fck ** (2 / 3)
        # self.__fctk_m = 0.3 * np.pow(self.__fck, 2/3) / 10  # em kN/cm2
        self._fctk_m = self.calcular_fct_m()
        self.__fctk_sup = 1.3 * self._fctk_m  # em kN/cm2
        self.__fctk_inf = 0.7 * self._fctk_m  # em kN/cm2
        # print(f"fck :{self.__fck}\tfct_m :{self.__fctk_m} fctk_sup: {self.__fctk_sup}")
        self.__alfa_e = tipo_agregado.value
        self.__eci = self.calcular_Eci()  # kN/cm2
        self.__alfa_i = min(0.8 + 0.2 * self.__fck / 80, 1)
        self.__ecs = self.__alfa_i * self.__eci
        self.__alfa_c = self.calcular_alfa_c()
        # faccio
        # self.__beta_lim, self.__alfa, self.__eta = .45, .85, .45 if self.__fck <= 50 else .35, .35, .35
        self._beta_lim, self._alfa, self._lambdaa, self._eta = (
            .45 if self.__fck <= 50 else .35,
            .85 if self.__fck <= 50 else 0.85 * (1 - (self.__fck - 50) / 200),
            .8 if self.__fck <= 50 else 0.8 - (self.fck - 50) / 400,
            1 if self.__fck <= 40 else pow(40 / self.__fck, 1 / 3)
        )

        self.__talRd2 = self.calcular_tal_Rd2()
        print(
            f"Concreto\nfck: {self.__fck} MPa\t alfai: {round(self.__alfa_i, 3)}\t Eci: {int(self.__eci)} MPa\t Ecs: {int(self.__ecs)} MPa")
        print(
            f"fcd: {self.__fcd:.4f} kN/cm2\tfctk m: {self._fctk_m:.4f} kN/cm2\tfctk sup: {self.__fctk_sup:.4f} kN/cm2\tfctk inf: {self.__fctk_inf:.4f} kN/cm2")

    def calcular_fcj(j: int, tipo_cimento: str):
        """
        Função retirada do curso de concreto prof. Bernardo Tutikian - Aula 4 da introdução do curso (8:37 min)
        """
        if tipo_cimento == 'cpi' or tipo_cimento == 'cpii':
            S = 0.2
        elif tipo_cimento == 'cpiii' or tipo_cimento == 'cpiv':
            S = 0.25
        elif tipo_cimento == 'cpv':
            S = 0.38
        else:  # NBR 6118
            S = 0.1545
        # print(j)
        # print(tipo_cimento)
        # print(S)
        # print(np.e)
        fcj = np.e ** (S * (1 - (25 / j) ** 0.5))
        return fcj

    def calcular_Eci(self):
        if self.__fck <= 50:
            Eci = self.__alfa_e * 5600 * (self.__fck ** 0.5)
        else:
            Eci = 21500 * self.__alfa_e * ((self.__fck / 10 + 1.25) ** (1 / 3))
        return int(Eci)

    def calcular_fct_m(self):
        if self.__fck <= 50:
            return 0.3 * np.pow(self.__fck, 2 / 3) / 10  # em kN/cm2
        else:
            return 2.12 * np.log(1 + 0.11 * self.__fck) / 10  # em kN/cm2

    def calcular_eta_c(self):
        if self.__fck <= 40:
            return 1.
        else:
            return pow(40 / self.__fck, 1 / 3)

    def calcular_alfa_c(self):
        if self.__fck <= 50:
            return 0.85
        else:
            return 0.85 * (1 - (self.__fck - 50) / 200)

    def x_duct(self):

        if self.fck <= 50:
            return 0.45
        else:
            return 0.35

    def calcular_lambda(self):
        if self.__fck <= 50:
            return 0.8
        else:
            return 0.8 - (self.fck - 50) / 400

    def epsilon_c2(self):
        if self.__fck <= 50:
            return 2. / 1000.
        else:
            return 2. / 1000. + ((0.085 / 1000.) * (self.__fck - 50) ** 0.53)

    def epsilon_cu(self):
        if self.__fck <= 50:
            return 3.5 / 1000.
        else:
            return 2.6 / 1000. + ((35. / 1000.) * ((90 - self.__fck) / 100.) ** 4)

    def calcular_ro_min(self):
        match self.__fck:
            case 20 | 25 | 30:
                return 0.15 / 100
            case 35:
                return 0.164 / 100
            case 40:
                return 0.179 / 100
            case 45:
                return 0.194 / 100
            case 50:
                return 0.208 / 100
            case 55:
                return 0.211 / 100
            case 60:
                return 0.219 / 100
            case 65:
                return 0.226 / 100
            case 70:
                return 0.233 / 100
            case 75:
                return 0.239 / 100
            case 80:
                return 0.245 / 100
            case 85:
                return 0.251 / 100
            case 90:
                return 0.256 / 100
            case _:
                return 0
                # return f"Valor de fck {self.__concreto.fck} inválido"

    def calcular_tal_Rd2(self):
        return 0.27 * (1 - self.__fck / 250) * self.__fcd

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

    @property
    def tal_Rd2(self):
        return self.__talRd2

    @property
    def alfa_c(self):
        return self.__alfa_c

    @property
    def eta_c(self):
        return self.__eta_c

    @property
    def lambdaa(self):
        return self._lambdaa
