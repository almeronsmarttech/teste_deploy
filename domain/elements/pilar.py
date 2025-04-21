#from  Concreto import Concreto
#from Aco import Aco
#from SecaoPilar import SecaoPilar
#from Esforcos import Esforcos
from domain.materials.concreto import Concreto
from domain.materials.aco import Aco, Barra


class Pilar:
    def __init__(self: object, lx: int = 19, ly: int = 19, lex: int = 300, ley: int = 300,
                 conc: Concreto = Concreto(25), esf: Esforcos = Esforcos(100, 0, 0, 0, 0),
                 aco: Aco = Aco(500), cobrimento: int = 3, fi_t: float = 5.0, fi_l: float = 12.5,
                 num_barras: int = 10) -> None:

        self.__hx = lx
        self.__hy = ly

        self.__A = self.__hx * self.__hy  # área bruta
        self.__Ac = self.__A  # menos a armadura - área líquida
        self.__lex = lex
        self.__ley = ley
        self.__Ro_min = 0.004 * self.__A
        self.__Ro_max = 0.04 * self.__A
        self.__cobrimento = cobrimento
        self.__As_efe = 0
        self.__As_calc = 0

        # Materiais
        self.__aco = aco
        self.__conc = conc

        # Esforços / carregamentos
        self.__esf = esf
        if min(self.__hx, self.__hy) < 19 and min(self.__hx, self.__hy) >= 14:
            gaman = 1.95 - 0.05 * self.__b
            self.__esf.NSd * gaman

        self.__M1dmin_x = self.momento_minimo(self.__hx)
        self.__M1dmin_y = self.momento_minimo(self.__hy)

        # Adimensionais
        self.__ni_calc = self.__esf.NSd / (self.__Ac * self.__conc.fcd)
        self.__ni_adot = max(self.__ni_calc, 0.5)
        # self.__mi =
        self.__MAx, self.__MBx = max(abs(self.__esf.Mdx_topo), abs(
            self.__esf.Mdx_base), self.__M1dmin_x), min(abs(self.__esf.Mdx_topo), abs(self.__esf.Mdx_base))
        # Verifica se o MxB tem que ser negativo
        if (self.__esf.Mdx_topo < 0 and self.__esf.Mdx_base > 0) or (
                self.__esf.Mdx_topo > 0 and self.__esf.Mdx_base < 0):
            self.__MBx *= -1
        self.__e1x = self.__MAx / self.__esf.NSd

        self.__lambdax = ((12) ** 0.5) * self.__lex / self.__hx
        self.__alfabx = 0.4
        if self.__MAx == self.__M1dmin_x:
            self.__alfabx = 1.0
        else:
            self.__alfabx = min(max(0.6 + 0.4 * self.__MxB / self.__MxA, 0.4), 1.0)

        self.__lambda1x_calc = (25 + 12.5 * (self.__e1x / self.__hx)) / self.__alfabx
        self.__lambda1x_adot = min(max(self.__lambda1x_calc, 35), 90)

        self.__MAy, self.__MBy = max(abs(self.__esf.Mdy_topo), abs(
            self.__esf.Mdy_base), self.__M1dmin_y), min(abs(self.__esf.Mdy_topo), abs(self.__esf.Mdy_base))
        if (self.__esf.Mdy_topo < 0 and self.__esf.Mdy_base > 0) or (
                self.__esf.Mdy_topo > 0 and self.__esf.Mdy_base < 0):
            self.__MBy *= -1
        self.__e1y = self.__MAy / self.__esf.NSd
        self.__lambday = ((12) ** 0.5) * self.__ley / self.__hy
        self.__alfaby = 0.4
        if self.__MAy == self.__M1dmin_y:
            self.__alfaby = 1
        else:
            self.__alfaby = min(max(0.6 + 0.4 * self.__MBy / self.__MAy, 0.4), 1.0)

        self.__lambda1y_calc = (25 + 12.5 * (self.__e1y / self.__hy)) / self.__alfaby
        self.__lambda1y_adot = min(max(self.__lambda1y_calc, 35), 90)

        self.__curvatura_x = self.pilar_padrao_curvatura_aproximada(self.__hx)
        self.__e2x = ((self.__lex ** 2) / 10) * self.__curvatura_x
        self.__M2dx = self.__esf.NSd * self.__e2x
        self.__Mdtotx = self.__alfabx * self.__MAx + self.__M2dx
        self.__rigidez_capa_aprox_x = self.pilar_padrao_rigidez_kapa_aproximada(self.__hx, self.__alfabx, self.__MAx,
                                                                                self.__lex)
        self.__curvatura_y = self.pilar_padrao_curvatura_aproximada(self.__hy)
        self.__e2y = ((self.__ley ** 2) / 10) * self.__curvatura_x
        self.__M2dy = self.__esf.NSd * self.__e2y
        self.__Mdtoty = self.__alfaby * self.__MAy + self.__M2dy
        self.__rigidez_capa_aprox_y = self.pilar_padrao_rigidez_kapa_aproximada(self.__hy, self.__alfaby, self.__MAy,
                                                                                self.__ley)

    def __str__(self: object) -> str:
        dados = f"\nDADOS DO PILAR:\n\nhx: {self.__hx} cm\thy: {self.__hy} cm\tlex: {self.__lex} cm\tley: {self.__ley} cm\n" \
                f"\nRESISTÊNCIAS: \n\n\t Resistências Características:\n fck: {round(self.__conc.fck, 2)} kN/cm2\tfyk: {round(self.__aco.fyk, 2)} kN/cm2" \
                f"\n\tResitências de Cáculo:\n fcd: {round(self.__conc.fcd, 2)} kN/cm2\tfyd: {round(self.__aco.fyd, 2)} kN/cm2\n" \
                f"\nESFORÇOS:\n\n {self.__esf}" \
                f"\nMOMENTOS MÍNIMOS:\n\n M1dmin_x: {round(self.__M1dmin_x, 2)} kN.cm\tM1dmin_y: {round(self.__M1dmin_y, 2)} kN.cm\n" \
                f"\nADIMENSIONAIS:\n\n" \
                f"\tν calc: {round(self.__ni_calc, 2)}\tν adot: {round(self.__ni_adot, 2)}\n" \
                f"\nÍNDICE DE ESBELTEZ:\n\n \tλx: {round(self.__lambdax, 2)}\tλy: {round(self.__lambday, 2)}\n" \
                f"\nÍNDICE DE ESBELTEZ LIMITE:\n\n \tλ1_x_calc: {round(self.__lambda1x_calc, 2)}\tλ_y_calc: {round(self.__lambda1y_calc, 2)}\n" \
                f"\n \tλ1_x_adot: {round(self.__lambda1x_adot, 2)}\tλ1_y_adot: {round(self.__lambda1y_adot, 2)}\n" \
                f"\nCURVATURA APROXIMADA:\n\n \t1_r_x: {round(self.__curvatura_x, 6)}\t1_r_y: {round(self.__curvatura_y, 6)}" \
                f"\n\tMdtotx: {round(self.__Mdtotx, 2)}\tMdtoty: {round(self.__Mdtoty, 2)}\n" \
                f"\nRIGIDEZ KAPA APROXIMADA:\n\n \tk_x: {round(self.__rigidez_capa_aprox_x, 2)}\tk_y: {round(self.__rigidez_capa_aprox_y, 2)}\n"

        if self.__lambdax < self.__lambda1x_adot:
            conclusao_x = "Os esforços de 2º ordem não são significativos em x."

        else:
            conclusao_x = "Tem que calcular os esforços de 2º ordem em x."

        if self.__lambday < self.__lambda1y_adot:
            conclusao_y = "Os esforços de 2º ordem não são significativos em y."
        else:
            conclusao_y = "Tem que calcular os esforços de 2º ordem em y."

        return dados + "\n" + conclusao_x + "\n" + conclusao_y
        # f"\nEM x:\n" \
        # f"\tlambdax: {round(self.__lambdax, 2)}" \
        # f"\te1x: {round(self.__e1x, 4)}"  # \

        # f"\te1x/lx: {round(self.__e1x_rel, 4)}" \
        # f"\nEM y:\n" \
        # f"\tlambday: {round(self.__lambday, 2)}" \
        # f"\te1y: {round(self.__e1y, 4)}" \
        # f"\te1y/ly: {round(self.__e1y_rel, 4)}"   \
        # f"\nMyA: {round(self.__MyA, 2)}\tMyB: {round(self.__MyB, 2)}\n" \
        # f"\talfaby: {round(self.__alfaby, 2)}" \
        # f"\tlambda1x: {round(self.__lambda1x_calc, 2)}" \
        # f"\talfabx: {round(self.__alfabx, 2)}" \
        # f"\nMxA: {round(self.__MxA, 2)}\tMxB: {round(self.__MxB, 2)}\n" \
        # f"\tlambda1y: {round(self.__lambda1y_calc, 2)}" \

    def armadura_minima_absoluta(self):
        return self.concreto.ro_min * self.b * self.h

    def calcula_momento_ductil(self):
        return self.concreto.alfa_c * self.concreto.eta_c * self.concreto.fcd * self.b * self.concreto.lambda_c * self.x_duct * (
                    self.d - self.concreto.lambda_c * self.x_duct / 2.)

    def pilar_padrao_curvatura_aproximada(self, dimensao):
        return min(0.005 / (dimensao * (self.__ni_adot + 0.5)), 0.005 / dimensao)

    # import math
    def pilar_padrao_rigidez_kapa_aproximada(self, dimensao, alfab, M1dA, le):
        dimensao /= 100
        M1dA /= 100
        le /= 100
        print(f"b: {dimensao}")
        print(f"NSd: {self.__esf.NSd}")
        print(f"M: {M1dA}")
        print(f"le: {le}")
        A = 5 * dimensao
        B = (dimensao ** 2) * self.__esf.NSd - ((self.__esf.NSd * ((le) ** 2)) / 320) - 5 * dimensao * alfab * M1dA
        C = - self.__esf.NSd * (dimensao ** 2) * alfab * M1dA
        print(f"A: {A}\tB: {B}\tC: {C}")
        return (-B + (B ** 2 - 4 * A * C) ** 0.5) / (2 * A)

    def momento_minimo(self, dim):
        return self.__esf.NSd * (1.5 + 0.03 * dim)

    def indice_esbeltez(self, dim, le):
        return math.sqrt(12) * le / dim

    def plotar_envoltorias_1a_2a_ordem(self):
        import matplotlib.pyplot as plt
        import numpy as np
        plt.style.use("ggplot")
        idade = np.array([0, 1, 3, 7, 28])

        Mx = np.array([self.__M1dmin_x, -self.__M1dmin_x])
        Mx_y = np.array([0, 0])
        My = np.array([self.__M1dmin_y, -self.__M1dmin_y])
        My_x = np.array([0, 0])
        # label = ['CP II', 'CP IV', 'CP V']
        x_1a_ordem = np.linspace(0, self.__M1dmin_x, 100)
        y_1a_ordem = self.__M1dmin_y * ((1 - ((x_1a_ordem ** 2) / (self.__M1dmin_x ** 2))) ** 0.5)
        print(y_1a_ordem)

        x_2a_ordem = np.linspace(0, self.__rigidez_capa_aprox_x * 100, 100)
        y_2a_ordem = self.__rigidez_capa_aprox_y * 100 * ((1 - ((x_1a_ordem ** 2) / (self.__M1dmin_x ** 2))) ** 0.5)
        print(y_1a_ordem)

        # plt.scatter(Mx, Mx_y, color = 'hotpink')
        # plt.scatter( My_x, My, color = 'blue')
        plt.plot(x_1a_ordem, y_1a_ordem, color='hotpink')

        plt.plot(x_1a_ordem, -y_1a_ordem, color='hotpink')
        plt.plot(-x_1a_ordem, y_1a_ordem, color='hotpink')
        plt.plot(-x_1a_ordem, -y_1a_ordem, color='hotpink')

        plt.plot(x_2a_ordem, y_2a_ordem, color='blue')
        # plt.fill(0,0, color = 'blue', alpha=0.25)
        plt.plot(x_2a_ordem, -y_2a_ordem, color='blue')
        plt.plot(-x_2a_ordem, y_2a_ordem, color='blue')
        plt.plot(-x_2a_ordem, -y_2a_ordem, color='blue')

        plt.fill(x_1a_ordem, y_1a_ordem, color='hotpink', alpha=0.25)
        plt.fill(x_1a_ordem, -y_1a_ordem, color='hotpink', alpha=0.25)

        plt.xlabel("Envoltória de Momentos em X (kN.cm)")
        plt.ylabel("Envoltória de Momentos em Y (kN.cm)")
        plt.show()

    def VerificaSeEhPilar(self: object) -> bool:
        # Verificar se tem as dimensoes mínimas e se não é pilar parede
        pass

    # def MomentoMinimo(self: object):

    #    print(f"Mdx_min: {round(Mxmin,2)}\tMdy_min: {round(Mymin,2)}")
    def CurvaResistente(self: object) -> None:
        print(
            f'Taxa As min = {self.__Ro_min} cm2\tTaxa As max = {self.__Ro_max} cm2')
        # num_barras = 10
        # Artigo
        d = 5  # cobrimento + estribo + meia barra longitudinal
        d1 = self.__cobrimento + self.__fi_t + self.__fi_l / 2
        print(f'd linha = {d1}')
        As_barra = 3.141593 * self.__fi_t * self.__fi_t / 4
        self.__As = As_barra * self.__num_barras
        self.__As = 25.968
        fy = 42  # kN/cm2
        maxTracao = self.__As * fy  # self.__aco.fyd     30 MPa 3 kN/cm2   --> 500 MPa 50kN/cm2
        print(f'NSd min = {round(maxTracao, 2)} kN')
        # parte do concreto                     # parte do aço -> es x deformação
        # maxCompressao = (self.__A - self.__As)*self.__conc.fcd * \
        #    0.85 + (self.__As*21000 * 0.002)
        maxCompressao = (self.__A * 0.85 * self.__conc.fck) + (self.__As * fy)
        print(f'NSd max = {round(maxCompressao, 2)} kN')

        # MÁX COMP E MÁX TRAÇÃO
        # secaoBalanceada =



