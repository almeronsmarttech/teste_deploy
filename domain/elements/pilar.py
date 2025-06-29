#from  Concreto import Concreto
#from Aco import Aco
#from SecaoPilar import SecaoPilar
#from Esforcos import Esforcos
import math

from domain.codes.nbr_6118_2023 import cobrimento
from domain.materials.concreto import Concreto
from domain.materials.aco import Aco, Barra
from domain.structure.estrutura import Estrutura
from domain.utils.geral import bhaskara, mais_proximo


class PilarRetangular:
    def __init__(self: object, hx: int = 19, hy: int = 19, lex: int = 300, ley: int = 300,
                 #conc: Concreto = Concreto(25),
                 Nk = 0, Mkx_topo = 0, Mkx_base = 0,Mky_topo = 0, Mky_base = 0,
                 estrutura=Estrutura(),
                 #esf: Esforcos = Esforcos(100, 0, 0, 0, 0),
                 #aco: Aco = Aco(500), cobrimento: int = 3,
                 fi_t: float = 5.0, fi_l: float = 12.5,
                 num_barras: int = 10) -> None:

        self.__hx = hx
        self.__hy = hy

        self.__A = self.__hx * self.__hy  # área bruta
        self.__Ac = self.__A  # menos a armadura - área líquida
        self.__lex = lex
        self.__ley = ley
        self.__dl = 5
        # ************************* AJUSTAR PARA A OUTRA DIREÇÃO TAMBÉM
        self.__d = self.__hy - self.__dl
        self.__h = self.__hy
        # *************************************************************
        self.__Ro_min = 0.004 * self.__A
        self.__Ro_max = 0.04 * self.__A
        self._estrutura = estrutura
        self.__cobrimento = self.cobrimento()
        self.__As_efe = 0
        self.__As_calc = 0
        self.__Asw = 0

        # Materiais
        self.__aco = estrutura.aco
        self.__conc = estrutura.concreto

        # Esforços / carregamentos
        #self.__esf = esf
        self.__Nk = Nk
        self.__Mkx_topo = Mkx_topo
        self.__Mkx_base = Mkx_base
        self.__Mky_topo = Mky_topo
        self.__Mky_base = Mky_base

        self.__NSd = self.__Nk * self._estrutura.gama_F
        self.__Mdx_base = self.__Mkx_base * self._estrutura.gama_F
        self.__Mdx_topo = self.__Mkx_topo * self._estrutura.gama_F
        self.__Mdy_base = self.__Mky_base * self._estrutura.gama_F
        self.__Mdy_topo = self.__Mky_topo * self._estrutura.gama_F

        if min(self.__hx, self.__hy) < 19 and min(self.__hx, self.__hy) >= 14:
            gaman = 1.95 - 0.05 * min(self.__hx, self.__hy)
            self.__NSd * gaman

        self.__M1dmin_x = self.momento_minimo(self.__hx)
        self.__M1dmin_y = self.momento_minimo(self.__hy)

        # Adimensionais
        self.__ni_calc = self.__NSd / (self.__Ac * self.__conc.fcd)
        self.__ni_adot = max(self.__ni_calc, 0.5)
        # self.__mi =
        self.__MAx, self.__MBx = max(abs(self.__Mdx_topo), abs(
            self.__Mdx_base), self.__M1dmin_x), min(abs(self.__Mdx_topo), abs(self.__Mdx_base))
        # Verifica se o MxB tem que ser negativo
        if (self.__Mdx_topo < 0 and self.__Mdx_base > 0) or (
                self.__Mdx_topo > 0 and self.__Mdx_base < 0):
            self.__MBx *= -1
        self.__e1x = self.__MAx / self.__NSd

        self.__lambdax = ((12) ** 0.5) * self.__lex / self.__hx
        self.__alfabx = 0.4
        if self.__MAx == self.__M1dmin_x:
            self.__alfabx = 1.0
        else:
            self.__alfabx = min(max(0.6 + 0.4 * self.__MBx / self.__MAx, 0.4), 1.0)

        self.__lambda1x_calc = (25 + 12.5 * (self.__e1x / self.__hx)) / self.__alfabx
        self.__lambda1x_adot = min(max(self.__lambda1x_calc, 35), 90)

        self.__MAy, self.__MBy = max(abs(self.__Mdy_topo), abs(
            self.__Mdy_base), self.__M1dmin_y), min(abs(self.__Mdy_topo), abs(self.__Mdy_base))
        if (self.__Mdy_topo < 0 and self.__Mdy_base > 0) or (
                self.__Mdy_topo > 0 and self.__Mdy_base < 0):
            self.__MBy *= -1
        self.__e1y = self.__MAy / self.__NSd
        self.__lambday = ((12) ** 0.5) * self.__ley / self.__hy
        self.__alfaby = 0.4
        if self.__MAy == self.__M1dmin_y:
            self.__alfaby = 1
        else:
            self.__alfaby = min(max(0.6 + 0.4 * self.__MBy / self.__MAy, 0.4), 1.0)

        self.__lambda1y_calc = (25 + 12.5 * (self.__e1y / self.__hy)) / self.__alfaby
        self.__lambda1y_adot = min(max(self.__lambda1y_calc, 35), 90)

        #self.__Mdtotx, self.__Mdtoty = 0,0

        self.__curvatura_x = self.pilar_padrao_curvatura_aproximada(self.__hx)
        self.__e2x = ((self.__lex ** 2) / 10) * self.__curvatura_x
        self.__M2dx = self.__NSd * self.__e2x
        self.__Mdtotx = self.__alfabx * self.__MAx + self.__M2dx
        if self.__lambda1x_adot > self.__lambdax:
            self.__Mdtotx = self.__MAx
        #self.__rigidez_capa_aprox_x = self.pilar_padrao_rigidez_kapa_aproximada(self.__hx, self.__alfabx, self.__MAx,
        #                                                                        self.__lex)
        self.__curvatura_y = self.pilar_padrao_curvatura_aproximada(self.__hy)
        self.__e2y = ((self.__ley ** 2) / 10) * self.__curvatura_y
        self.__M2dy = self.__NSd * self.__e2y
        self.__Mdtoty = self.__alfaby * self.__MAy + self.__M2dy
        if self.__lambda1y_adot > self.__lambday:
            self.__Mdtoty = self.__MAy
#        self.__rigidez_capa_aprox_y = self.pilar_padrao_rigidez_kapa_aproximada(self.__hy, self.__alfaby, self.__MAy,
#                                                                                self.__ley)
    @property
    def Mdx_topo(self):
        return self.__Mdx_topo

    @property
    def Mdx_base(self):
        return self.__Mdx_base

    @property
    def Mdy_topo(self):
        return self.__Mdy_topo

    @property
    def Mdy_base(self):
        return self.__Mdy_base

    @property
    def NSd(self):
        return self.__NSd

    def __str__(self: object) -> str:
        dados = f"\nDADOS DO PILAR:\n\nhx: {self.__hx} cm\thy: {self.__hy} cm\tlex: {self.__lex} cm\tley: {self.__ley} cm\n" \
                f"\nRESISTÊNCIAS: \n\n\t Resistências Características:\n fck: {round(self.__conc.fck, 2)} kN/cm2\tfyk: {round(self.__aco.fyk, 2)} kN/cm2" \
                f"\n\tResitências de Cáculo:\n fcd: {round(self.__conc.fcd, 2)} kN/cm2\tfyd: {round(self.__aco.fyd, 2)} kN/cm2\n" \
                f"\nESFORÇOS:\n\n Nsd: {self.__NSd}\t Mdx topo: {self.__Mdx_topo} kN.cm\t Mdx base: {self.__Mdx_base} kN.cm\t Mdy topo: {self.__Mdy_topo} kN.cm\t Mdy base: {self.__Mdy_base} kN.cm\n" \
                f"\nMOMENTOS MÍNIMOS:\n\n M1dmin_x: {round(self.__M1dmin_x, 2)} kN.cm\tM1dmin_y: {round(self.__M1dmin_y, 2)} kN.cm\n" \
                f"\nADIMENSIONAIS:\n\n" \
                f"\tν calc: {round(self.__ni_calc, 2)}\tν adot: {round(self.__ni_adot, 2)}\n" \
                f"\nÍNDICE DE ESBELTEZ:\n\n \tλx: {round(self.__lambdax, 2)}\tλy: {round(self.__lambday, 2)}\n" \
                f"\nÍNDICE DE ESBELTEZ LIMITE:\n\n \tλ1_x_calc: {round(self.__lambda1x_calc, 2)}\tλ_y_calc: {round(self.__lambda1y_calc, 2)}\n" \
                f"\n \tλ1_x_adot: {round(self.__lambda1x_adot, 2)}\tλ1_y_adot: {round(self.__lambda1y_adot, 2)}\n" \
                #f"\nCURVATURA APROXIMADA:\n\n \t1_r_x: {round(self.__curvatura_x, 6)}\t1_r_y: {round(self.__curvatura_y, 6)}" \
                #f"\n\talfab_x: {round(self.__alfabx, 2)}\talfab_y: {round(self.__alfaby, 2)}\n" \
                #f"\n\tMdtotx: {round(self.__Mdtotx, 2)}\tMdtoty: {round(self.__Mdtoty, 2)}\n" \
                #f"\nRIGIDEZ KAPA APROXIMADA:\n\n \tk_x: {round(self.__rigidez_capa_aprox_x, 2)}\tk_y: {round(self.__rigidez_capa_aprox_y, 2)}\n"

        if self.__lambdax < self.__lambda1x_adot:
            self.__Mdtotx = self.__MAx
            conclusao_x = "Os esforços de 2º ordem não são significativos em x."

        else:
            #self.__curvatura_x = self.pilar_padrao_curvatura_aproximada(self.__hx)
            #self.__e2x = ((self.__lex ** 2) / 10) * self.__curvatura_x
            #self.__M2dx = self.__NSd * self.__e2x
            self.__Mdtotx = self.__alfabx * self.__MAx + self.__M2dx
            conclusao_x = "Tem que calcular os esforços de 2º ordem em x."


        if self.__lambday < self.__lambda1y_adot:
            self.__Mdtoty = self.__MAy
            conclusao_y = "Os esforços de 2º ordem não são significativos em y."
        else:
            self.__curvatura_y = self.pilar_padrao_curvatura_aproximada(self.__hy)
            #self.__e2y = ((self.__ley ** 2) / 10) * self.__curvatura_y
            #self.__M2dy = self.__NSd * self.__e2y
            self.__Mdtoty = self.__alfaby * self.__MAy + self.__M2dy
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

    def resultados(self):
        return round(self.__Mdtotx,2), round(self.__Mdtoty,2) # self.__Mdtotx, self.__Mdtoty, self.__Mdtotx, self.__Mdtoty

    def cobrimento(self):
        return self._estrutura.cobrimento_nominal("pilar")

    def armadura_minima_absoluta(self):
        return self.concreto.ro_min * self.b * self.h

    def calcula_momento_ductil(self):
        return self.concreto.alfa_c * self.concreto.eta_c * self.concreto.fcd * self.b * self.concreto.lambda_c * self.x_duct * (
                    self.d - self.concreto.lambda_c * self.x_duct / 2.)

    def pilar_padrao_curvatura_aproximada(self, dimensao):
        return min(0.005 / (dimensao * (self.__ni_adot + 0.5)), 0.005 / dimensao)

    def dominio_deformacao(self, x_estrela, x_2_3, x_lim):
        if x_estrela < 0:
            print("Domínio 1")
            eps_c = -10 * (x_estrela / (self.__d - x_estrela)) / 1000
            eps_1 = 10 / 1000
            eps_2 = 10 * ((self.__dl - x_estrela) / (self.__d - x_estrela)) / 1000

        elif x_estrela < x_2_3:
            print("Domínio 2")
            eps_c = 10 * (x_estrela / (self.__d - x_estrela)) / 1000
            eps_1 = 10 / 1000
            eps_2 = 10 * ((x_estrela - self.__dl) / (self.__d - x_estrela)) / 1000
            print(eps_2)
        elif x_estrela < x_lim:
            print("Domínio 3")
            eps_c = 3.5 / 1000
            eps_1 = 3.5 * ((self.__d - x_estrela) / x_estrela) / 1000
            eps_2 = 3.5 * ((x_estrela - self.__dl) / x_estrela) / 1000

        elif x_estrela < self.__d:
            print("Domínio 4")
            eps_c = 3.5 / 1000
            eps_1 = 3.5 * ((self.__d - x_estrela) / x_estrela) / 1000
            eps_2 = 3.5 * ((x_estrela - self.__dl) / x_estrela) / 1000

        elif x_estrela < self.__h:
            print("Domínio 4a")
            eps_c = 3.5 / 1000
            eps_1 = 3.5 * ((self.__d - x_estrela) / x_estrela) / 1000
            eps_2 = 3.5 * ((x_estrela - self.__dl) / x_estrela) / 1000

        else:  # x_estrela > h
            print("Domínio 5")
            divisor = (x_estrela - (3 / 7) * self.__h)
            eps_c = 2 * (x_estrela / divisor) / 1000
            eps_1 = 2 * ((x_estrela - self.__d) / divisor) / 1000
            eps_2 = 2 * ((x_estrela - self.__dl) / divisor) / 1000

        #eps_c, eps1, eps2 = eps_c / 1000, eps_1 / 1000, eps_2 / 1000
        sigma_1_estrela, sigma_2_estrela = self.Tensoes(eps_1, eps_2)
        return eps_c, eps_1, eps_2, sigma_1_estrela, sigma_2_estrela

    def Tensoes(self, eps_1, eps_2):
        print(f"Função Tensões:\neps1: {eps_1}, eps2: {eps_2}, epsilon_y_d: {self.__aco.epsilon_y_d}")
        if (eps_1<self.__aco.epsilon_y_d):
            sigma_1_estrela = self.__aco._es * eps_1
        else:
            sigma_1_estrela = self.__aco.fyd

        if (eps_2<self.__aco.epsilon_y_d):
            sigma_2_estrela = self.__aco._es * eps_2
        else:
            sigma_2_estrela = self.__aco.fyd

        return sigma_1_estrela, sigma_2_estrela

    def iterar_As1_As2(self, x, x_2_3, x_lim, A1, B1, C1, A2, B2, C2, b,max_iter=100, tolerancia=0.001, min_iter=5):
        x_arb = x / 2
        D = self.__conc.alfa_c * self.__conc.lambdaa * self.__conc.fcd * b
        #min_iter = 5  # Número mínimo de iterações

        for i in range(max_iter):
            # Etapa 1: calcular deformações e tensões
            eps_c, eps_1, eps_2, sigma_1_estrela, sigma_2_estrela = self.dominio_deformacao(x_arb, x_2_3, x_lim)

            # Calcular As1 e x_calc1
            As1 = (A1 * x_arb ** 2 + B1 * x_arb + C1) / sigma_1_estrela
            x_calc1 = (self.NSd - As1 * (sigma_2_estrela - sigma_1_estrela)) / D

            # Calcular As2 e x_calc2
            As2 = (A2 * x_arb ** 2 + B2 * x_arb + C2) / sigma_2_estrela
            x_calc2 = (self.NSd - As2 * (sigma_2_estrela - sigma_1_estrela)) / D

            # Verificar critério de convergência
            if i >= min_iter and abs(As1 - As2) / max(As1, As2) <= tolerancia:
                print(f"[Iter {i}] Convergência alcançada.")
                return As1, As2, x_arb

            # Atualizar x_arb
            x_arb = (x_arb + mais_proximo(x_arb, x_calc1, x_calc2)) / 2

        print("[Aviso] Máximo de iterações alcançado sem convergir.")
        return As1, As2, x_arb  # último valor

    def dimensionamento(self):
        # Para My
        b = self.__hx
        h = self.__hy
        dl = 5
        d = h - dl

        e_0 = self.Mdy_topo*100/self.__NSd
        e_1 = (d - dl)/2 + e_0
        e_2 = (d - dl)/2 - e_0
        print(f"e_0: {e_0}\te_1: {e_1}\te_2: {e_2}")

        e2_0 = (self.__NSd/(2*self.__conc.alfa_c*self.__conc.fcd*b))-dl

        x_2_3 = 0.259 * d
        x_lim = 0.628 * d

        e2_2_3 = (self.__conc.alfa_c * self.__conc.lambdaa * self.__conc.fcd * b * d *(0.5*self.__conc.lambdaa*d-dl))/self.__NSd

        Rcc_estrela = self.__conc.alfa_c * self.__conc.fcd * b * h # força do concreto em toda a seção comprimida
        x_estrela = h / self.__conc.lambdaa

        eps_c , eps_1, eps_2, sigma_1_estrela,  sigma_2_estrela= self.dominio_deformacao(x_estrela, x_2_3, x_lim)
        print(f"eps_c: {eps_c}\teps_1: {eps_1}\teps_2: {eps_2}\teps_y_d: {self.__aco.epsilon_y_d}")

        print(f"sigma_1_estrela: {sigma_1_estrela:.2f} kN/cm2\tsigma_2_estrela: {sigma_2_estrela:.2f} kN/cm2\t")
            
        e2_3_4 = ((d-dl)/2)*(1+((Rcc_estrela/self.NSd)-1)*((sigma_2_estrela-sigma_1_estrela)/(sigma_2_estrela+sigma_1_estrela)))
        print(f"x_2_3: {x_2_3}\tx_lim: {x_lim}\te2_0: {e2_0}\te2_2_3: {e2_2_3*self.__NSd}\tRcc_estrela: {Rcc_estrela}\tx_estrela:{x_estrela}\te2_3_4: {e2_3_4*self.__NSd}")
        e_2_0 = (self.__NSd/(2*self.__conc.alfa_c*self.__conc.fcd*b))-dl
        if e_2 < e_2_0:
            print("É necessário armar")
        else:
            print("Não é necessário armar")
        if e_2 < 0:
            print("Caso 1")
            A1 = (self.__conc.alfa_c * self.__conc.lambdaa * self.__conc.fcd * b * 0.5 * self.__conc.lambdaa) / (d - dl)
            B1 = (self.__conc.alfa_c * self.__conc.lambdaa * self.__conc.fcd * b * (-dl)) / (d - dl)
            C1 = self.NSd * abs(e_2) / (d - dl)
            print(f"A1 = {A1}\tB1 = {B1}\tC1 = {C1}")


            A2 = -(self.__conc.alfa_c * self.__conc.lambdaa * self.__conc.fcd * b * -0.5 * self.__conc.lambdaa) / (d - dl)
            B2 = -(self.__conc.alfa_c * self.__conc.lambdaa * self.__conc.fcd * b * d) / (d - dl)
            C2 = self.NSd * abs(e_1) / (d - dl)
            print(f"A2 = {A2}\tB2 = {B2}\tC2 = {C2}")
            possiveis_x = []
            if bhaskara(A1, B1, C1):
                x1, x2 = bhaskara(A1, B1, C1)
                possiveis_x.append(x1)
                possiveis_x.append(x2)
                print(f"x1 = {x1}\tx2 = {x2}")
            else:
                print("Não possui raizes reais")

            if bhaskara(A2, B2, C2):
                x3, x4 = bhaskara(A2, B2, C2)
                possiveis_x.append(x3)
                possiveis_x.append(x4)
                print(f"x3 = {x3}\tx4 = {x4}")
            else:
                print("Não possui raizes reais")

            x = None

            for xi in possiveis_x:
                if xi >= 0 and xi <= d:  # para o caso 1 (domínios 2, 3 e 4)
                    x = xi
            print(f"x = {x}")

            x_arb = x / 2
            As1, As2, x = self.iterar_As1_As2(x_arb,x_2_3,x_lim,A1,B1,C1,A2,B2,C2,b)
            print(f"As1 = {As1}\tAs2 = {As2}\tx = {x}")
            # x_arb = x / 2
            # eps_c , eps_1, eps_2, sigma_1_estrela, sigma_2_estrela = self.dominio_deformacao(x_arb,x_2_3,x_lim)
            # print(f"eps_c: {eps_c}\teps_1: {eps_1}\teps_2: {eps_2}\teps_y_d: {self.__aco.epsilon_y_d}\tsigma_1_estrela: {sigma_1_estrela}\tsigma_2_estrela: {sigma_2_estrela}")
            # D = (self.__conc.alfa_c * self.__conc.lambdaa * self.__conc.fcd * b)
            # As1, x_calc1, As2, x_calc2 = 0, 0, 0, 0
            # print(f"A1: {A1}\tx_arb: {x_arb}\tB1: {B1}\tC1: {C1}\tsimga_1_estrela: {sigma_1_estrela}")
            # As1 = (A1 * x_arb ** 2 + B1 * x_arb + C1) / sigma_1_estrela
            # x_calc1 = (self.NSd - As1 * (sigma_2_estrela - sigma_1_estrela)) / D
            # print(f"A2: {A2}\tx_arb: {x_arb}\tB2: {B2}\tC2: {C2}\tsimga_2_estrela: {sigma_2_estrela}")
            # As2 = (A2 * x_arb ** 2 + B2 * x_arb + C2) / sigma_2_estrela
            # x_calc2 = (self.NSd - As2 * (sigma_2_estrela - sigma_1_estrela)) / D
            # print(f"As1 = {As1}\tAs2 = {As2}\tx_calc1 = {x_calc1}\tx_calc2 = {x_calc2}")
            # x_arb2 = (x_arb + mais_proximo(x_arb,x_calc1,x_calc2)) / 2
            # print(f"x_arb2 = {x_arb2}")
            # eps_c, eps_1, eps_2, sigma_1_estrela, sigma_2_estrela = self.dominio_deformacao(x_arb2, x_2_3, x_lim)
            #
            # print(
            #     f"eps_c: {eps_c}\teps_1: {eps_1}\teps_2: {eps_2}\teps_y_d: {self.__aco.epsilon_y_d}\tsigma_1_estrela: {sigma_1_estrela}\tsigma_2_estrela: {sigma_2_estrela}")
            #
            # As1, x_calc1, As2, x_calc2 = 0, 0, 0, 0
            # print(f"A1: {A1}\tx_arb: {x_arb2}\tB1: {B1}\tC1: {C1}\tsimga_1_estrela: {sigma_1_estrela}")
            # As1 = (A1 * x_arb2 ** 2 + B1 * x_arb2 + C1) / sigma_1_estrela
            # x_calc1 = (self.NSd - As1 * (sigma_2_estrela - sigma_1_estrela)) / D
            # print(f"A2: {A2}\tx_arb: {x_arb2}\tB2: {B2}\tC2: {C2}\tsimga_2_estrela: {sigma_2_estrela}")
            # As2 = (A2 * x_arb2 ** 2 + B2 * x_arb2 + C2) / sigma_2_estrela
            # x_calc2 = (self.NSd - As2 * (sigma_2_estrela - sigma_1_estrela)) / D
            # print(f"As1 = {As1}\tAs2 = {As2}\tx_calc1 = {x_calc1}\tx_calc2 = {x_calc2}")
            # x_arb3 = (x_arb2 + mais_proximo(x_arb2, x_calc1, x_calc2)) / 2
            # print(f"x_arb3 = {x_arb3}")
            #
            # eps_c, eps_1, eps_2, sigma_1_estrela, sigma_2_estrela = self.dominio_deformacao(x_arb3, x_2_3, x_lim)
            #
            # print(
            #     f"eps_c: {eps_c}\teps_1: {eps_1}\teps_2: {eps_2}\teps_y_d: {self.__aco.epsilon_y_d}\tsigma_1_estrela: {sigma_1_estrela}\tsigma_2_estrela: {sigma_2_estrela}")
            #
            # As1, x_calc1, As2, x_calc2 = 0, 0, 0, 0
            # print(f"A1: {A1}\tx_arb: {x_arb3}\tB1: {B1}\tC1: {C1}\tsimga_1_estrela: {sigma_1_estrela}")
            # As1 = (A1 * x_arb3 ** 2 + B1 * x_arb3 + C1) / sigma_1_estrela
            # x_calc1 = (self.NSd - As1 * (sigma_2_estrela - sigma_1_estrela)) / D
            # print(f"A2: {A2}\tx_arb: {x_arb3}\tB2: {B2}\tC2: {C2}\tsimga_2_estrela: {sigma_2_estrela}")
            # As2 = (A2 * x_arb3 ** 2 + B2 * x_arb3 + C2) / sigma_2_estrela
            # x_calc2 = (self.NSd - As2 * (sigma_2_estrela - sigma_1_estrela)) / D
            # print(f"As1 = {As1}\tAs2 = {As2}\tx_calc1 = {x_calc1}\tx_calc2 = {x_calc2}")



        elif e_2 < e2_2_3:
            print("Caso 2")
        elif e_2 < e2_3_4:
            print("Caso 3")
        else:
            print("Caso 4")
    # import math
    # def pilar_padrao_rigidez_kapa_aproximada(self, dimensao, alfab, M1dA, le):
    #     dimensao /= 100
    #     M1dA /= 100
    #     le /= 100
    #     print(f"b: {dimensao}")
    #     print(f"NSd: {self.__NSd}")
    #     print(f"M: {M1dA}")
    #     print(f"le: {le}")
    #     A = 5 * dimensao
    #     B = (dimensao ** 2) * self.__NSd - ((self.__NSd * ((le) ** 2)) / 320) - 5 * dimensao * alfab * M1dA
    #     C = - self.__NSd * (dimensao ** 2) * alfab * M1dA
    #     print(f"A: {A}\tB: {B}\tC: {C}")
    #     return (-B + (B ** 2 - 4 * A * C) ** 0.5) / (2 * A)

    def momento_minimo(self, dim):
        return self.__NSd * (1.5 + 0.03 * dim)

    def indice_esbeltez(self, dim, le):
        return math.sqrt(12) * le / dim

    # def plotar_envoltorias_1a_2a_ordem(self):
    #     import matplotlib.pyplot as plt
    #     import numpy as np
    #     plt.style.use("ggplot")
    #     idade = np.array([0, 1, 3, 7, 28])
    #
    #     Mx = np.array([self.__M1dmin_x, -self.__M1dmin_x])
    #     Mx_y = np.array([0, 0])
    #     My = np.array([self.__M1dmin_y, -self.__M1dmin_y])
    #     My_x = np.array([0, 0])
    #     # label = ['CP II', 'CP IV', 'CP V']
    #     x_1a_ordem = np.linspace(0, self.__M1dmin_x, 100)
    #     y_1a_ordem = self.__M1dmin_y * ((1 - ((x_1a_ordem ** 2) / (self.__M1dmin_x ** 2))) ** 0.5)
    #     print(y_1a_ordem)
    #
    #     x_2a_ordem = np.linspace(0, self.__rigidez_capa_aprox_x * 100, 100)
    #     y_2a_ordem = self.__rigidez_capa_aprox_y * 100 * ((1 - ((x_1a_ordem ** 2) / (self.__M1dmin_x ** 2))) ** 0.5)
    #     print(y_1a_ordem)
    #
    #     # plt.scatter(Mx, Mx_y, color = 'hotpink')
    #     # plt.scatter( My_x, My, color = 'blue')
    #     plt.plot(x_1a_ordem, y_1a_ordem, color='hotpink')
    #
    #     plt.plot(x_1a_ordem, -y_1a_ordem, color='hotpink')
    #     plt.plot(-x_1a_ordem, y_1a_ordem, color='hotpink')
    #     plt.plot(-x_1a_ordem, -y_1a_ordem, color='hotpink')
    #
    #     plt.plot(x_2a_ordem, y_2a_ordem, color='blue')
    #     # plt.fill(0,0, color = 'blue', alpha=0.25)
    #     plt.plot(x_2a_ordem, -y_2a_ordem, color='blue')
    #     plt.plot(-x_2a_ordem, y_2a_ordem, color='blue')
    #     plt.plot(-x_2a_ordem, -y_2a_ordem, color='blue')
    #
    #     plt.fill(x_1a_ordem, y_1a_ordem, color='hotpink', alpha=0.25)
    #     plt.fill(x_1a_ordem, -y_1a_ordem, color='hotpink', alpha=0.25)
    #
    #     plt.xlabel("Envoltória de Momentos em X (kN.cm)")
    #     plt.ylabel("Envoltória de Momentos em Y (kN.cm)")
    #     plt.show()

    def VerificaSeEhPilar(self: object) -> bool:
        # Verificar se tem as dimensoes mínimas e se não é pilar parede
        pass

    # def MomentoMinimo(self: object):

    #    print(f"Mdx_min: {round(Mxmin,2)}\tMdy_min: {round(Mymin,2)}")

# def CurvaResistente(self: object) -> None:
#     print(
#         f'Taxa As min = {self.__Ro_min} cm2\tTaxa As max = {self.__Ro_max} cm2')
#     # num_barras = 10
#     # Artigo
#     d = 5  # cobrimento + estribo + meia barra longitudinal
#     d1 = self.__cobrimento + self.__fi_t + self.__fi_l / 2
#     print(f'd linha = {d1}')
#     As_barra = 3.141593 * self.__fi_t * self.__fi_t / 4
#     self.__As = As_barra * self.__num_barras
#     self.__As = 25.968
#     fy = 42  # kN/cm2
#     maxTracao = self.__As * fy  # self.__aco.fyd     30 MPa 3 kN/cm2   --> 500 MPa 50kN/cm2
#     print(f'NSd min = {round(maxTracao, 2)} kN')
#     # parte do concreto                     # parte do aço -> es x deformação
#     # maxCompressao = (self.__A - self.__As)*self.__conc.fcd * \
#     #    0.85 + (self.__As*21000 * 0.002)
#     maxCompressao = (self.__A * 0.85 * self.__conc.fck) + (self.__As * fy)
#     print(f'NSd max = {round(maxCompressao, 2)} kN')

    # MÁX COMP E MÁX TRAÇÃO
    # secaoBalanceada =
