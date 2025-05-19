import numpy as np

from domain.utils.parametros_araujo import *
from domain.materials.concreto import Concreto
from domain.materials.aco import Aco, Barra




class Laje:
    def __init__(self, lx: float, ly: float, h: int, g: float, q: float, tipo_laje: int, concreto: Concreto, aco:Aco, bitolas, psi2=0.4, cobrimento = 4.0, **kwargs):
        self._lx = lx
        self._ly = ly
        self._h = h
        self.__b = 100
        self._d = self._h - cobrimento
        self.__g = g
        self.__q = q
        self._p = self.__g + self.__q
        self.__psi2 = psi2
        self._p_serv =self.__g + self.__psi2 * self.__q
        #print(f"psi2: {self.__psi2}")
        #self._p_serv = self.__g + 0.3 * self.__q
        self._tipo_laje = tipo_laje
        self._concreto = concreto
        self.__aco = aco
        self._D = (self._concreto.Ecs * self._h / 10 * self._h / 10 * self._h / 10) / (12 * (1 - (self._concreto.nu * self._concreto.nu))) #  rigidez
        print(f"D: {int(self._D)} kN")
        self.__W0 = self.__b * self._h * self._h / 6  # módulo resistente cm3
        print(f"W0: {self.__W0:.2f} cm3")
        self._w0 = 0 # flecha inicial m
        self.__wf = 0  # flecha inicial m
        self._wlim = min(self._lx, self._ly) / 250
        self.__alfa_f = 0 #coeficiente multiplicador de flechas para consideração de fluência (cargas de longa duração)
        self.__Mdmin = 0.8 * self.__W0 * self._concreto.fctk_sup
        #print(f"Md_min: {self.__Mdmin:.2f} kN.cm/m")
        self._ro_min = self._concreto.calcular_ro_min()
        print(f"ro_min: {self._ro_min}")
        #self._As_min = max(self.__ro_min * self.__b * self.__h,self.calcular_As(self.__Mdmin))
        #self._As_min = self.calcular_As(self.__Mdmin/100)
        self._As_min = self._ro_min * self.__b * self._h
        self._Ase_min_bidirecional = 0
        self.__bitola_minima = 5.0 / 10 # em cm
        self.__bitola_maxima = self._h / 8 # em cm
        self.__bitolas = bitolas
        self.__bitolas_possiveis = []
        self.__espacamento_minimo = 8.0
        self.__espacamento_maximo = min(20.0, self._h * 2)
        #self._tal_Rd1 = self.calcular_tal_Rd1()


    def calcular_flecha_final(self, alfa_f=0, tempo_inicial_carregamento = 0, tempo_final_carregamento=71, ro_linha=0):
        # para carregamentos com 70 meses ou mais, xsi(t)=2
        # ro linha = 0 quando não existe armadura de compressão
        delta_xsi = self.calcular_xsi_t(tempo_final_carregamento) -  self.calcular_xsi_t(tempo_inicial_carregamento)
        if alfa_f == 0:
            self.__alfa_f = delta_xsi  / (1+50*ro_linha)
        else:
            self.__alfa_f = alfa_f
        self.__wf = self.__alfa_f * self._w0
        print(f"Flecha inicial: {self._w0*100:.4f} cm\tcoef. flecha diferida (alfa f): {self.__alfa_f:.2f}\tflecha final: {self.__wf*100:.4f} cm")
        return round(self.__wf*100,4)

    def calcular_flecha_limite(self):
        return round(self._wlim * 100, 4) # retorna flecha limite em cm

    def calcular_xsi_t(self, tempo_carregamento):
        if tempo_carregamento <= 70:
            return 0.68*(0.996**tempo_carregamento)*tempo_carregamento**0.32
        else:
            return 2

    def calcular_As(self, momento, gama_f = 1.4):
        momento = abs(momento)
        mi = (gama_f * momento * 100) / (self.__b * self._d * self._d * 0.85 * self._concreto.fcd)
        print(f"gama_f: {gama_f}\tmomento: {momento:.2f} kN.m\tb: {self.__b}\td: {self._d:.2f} cm\tfcd: {self._concreto.fcd:.4f} kN/cm2")
        xsi = (1-np.sqrt(1-2*mi))/0.8
        print(f"mi: {mi:.4f}\txsi: {xsi:.4f}")
        return 0.8*xsi*self.__b*self._d*0.85*self._concreto.fcd/self.__aco.fyd

    def calcular_As_min(self):
        # calcula a armadura mínima através do momento mínimo
        #as_min_mom_min = self.calcular_As(self.__Mdmin)
        as_min_mom_min = 1
        # calcula a armadura mínima através da taxa de armadura mínima
        #as_min_ro_min =
        #print(f"as_min_mom_min: {as_min_mom_min}\t as_min_ro_min: {as_min_ro_min}")
        #as_min = max(as_min_mom_min,as_min_ro_min)
        #return as_min



    def detalhamento_armaduras(self, As_necessario, cobertura = 1, tamanho = 1):
        self.__bitolas_possiveis = []
        lista_resposta =[]
        for bitola in self.__bitolas:
            if self.__bitola_minima <= bitola.diametro <= self.__bitola_maxima:
                self.__bitolas_possiveis.append(bitola)
        for bitola in self.__bitolas_possiveis:
            num_barras = As_necessario/ bitola.area_aco
            espacamento = int(np.floor(100 / num_barras))

            if espacamento > self.__espacamento_maximo:
                espacamento = self.__espacamento_maximo
                #recalcula número de barras
                num_barras = 100 / espacamento
            if espacamento > self.__espacamento_minimo:
                num_barras = int(np.ceil(num_barras * cobertura))
                print(
                    f"{num_barras} Φ de {bitola.diametro * 10:.1f} mm a cada {espacamento} cm.\tAs efetivo: {num_barras / cobertura * bitola.area_aco:.2f} cm2/m.")
                lista_resposta.append(
                    f"Φ de {bitola.diametro * 10:.1f} mm a cada {espacamento} cm. (As efetivo: {num_barras / cobertura * bitola.area_aco:.2f} cm2/m) -  N = {num_barras}    L = {tamanho:.2f} m ")

        return lista_resposta


    #def calcular_tal_Rd1(self):
    #    return 0.13*(1 - np.sqrt(20 / self._d))*np.pow(100 * () * self._concreto.fck, 1 / 3)

class LajeUnidirecional(Laje):
    def __init__(self, lx: float, ly: float, h: int, g: float, q: float, tipo_laje: int, concreto: Concreto, aco:Aco, bitolas, psi2=0.4):
        super().__init__(lx, ly, h, g, q, tipo_laje, concreto,aco,bitolas, psi2)
        self.__R = 0
        self.__Re = 0
        self.__M, self.__Me = 0, 0
        self.__As_calculada, self.__Ase_calculada, self.__As_secundaria = 0, 0, 0
        self.__As_adotada, self.__Ase_adotada = 0, 0
        self.__k = 0
        self.__gama_n = 1.0
        print(f"Laje Unidirecional tipo: {self._tipo_laje}")

    def calcular_reacoes_apoio(self):
        print("Calculo de reacoes de apoio")
        if self._tipo_laje == 1:
             self.__R = self._p * self._lx / 2.0
        elif self._tipo_laje == 2:
             self.__R = 3 * self._p * self._lx / 8.0
             self.__Re = 5 * self._p * self._lx / 8.0
        elif self._tipo_laje == 3:
             self.__Re = self._p * self._lx / 2.0
        elif self._tipo_laje == 4:
             self.__Re = self._p * self._lx
        else:
            print("Tipo de laje não encontrada")

        print(f"Rx : {self.__R:.2f} kN/m\tRxe : {self.__Re:.2f} kN/m")
        return round(self.__R, 2), round(self.__Re, 2)

    def calcular_momentos_fletores(self):
        print("Calculo dos momentos de fletores")
        if self._tipo_laje == 1:
            self.__M = self._p * self._lx * self._lx / 8.0
        elif self._tipo_laje == 2:
            self.__M = self._p * self._lx * self._lx / 14.22
            self.__Me = - self._p * self._lx * self._lx / 8.0
        elif self._tipo_laje == 3:
            self.__M = self._p * self._lx * self._lx / 24
            self.__Me = - self._p * self._lx * self._lx / 12
        elif self._tipo_laje == 4:
            self.__Me = - self._p * self._lx * self._lx / 2
            if self._h < 19:
                self.__gama_n = 1.95 - .05*self._h
                self.__Me *= self.__gama_n
                print(f"Momento negativo majorado por gama n = {self.__gama_n:.2f}")
        else:
            print("Tipo de laje não encontrada")

        print(f"Mx : {self.__M:.2f} kN.m/m\tMxe : {self.__Me:.2f} kN.m/m")
        return round(self.__M,2),round(self.__Me,2)

    def calcular_armaduras(self):
        if self.__M > 0:
            self.__As_calculada = self.calcular_As(self.__M)
        if abs(self.__Me) > 0:
            self.__Ase_calculada = self.calcular_As(self.__Me)
        as_sec1 =0.2 * self.__As_calculada
        as_sec2 = 0.9
        as_sec3 = 0.5 * self._As_min
        self.__As_secundaria = max(as_sec1, as_sec2, as_sec3)
        print(f"Armadura Calculada:\nAs+: {self.__As_calculada:.2f} cm2/m\tAs-: {self.__Ase_calculada:.2f} cm2/m\tAs_min: {self._As_min:.2f} cm2/m")
        print(f"As_sec1: {as_sec1:.2f} cm2/m\tAs_sec2: {as_sec2:.2f} cm2/m\tas_sec3: {as_sec3:.2f} cm2/m")
        if self.__As_calculada > 0:
            self.__As_adotada = max(self.__As_calculada, self._As_min)

        if self.__Ase_calculada > 0:
            self._Ase_min_bidirecional = self._As_min
            self.__Ase_adotada = max(self.__Ase_calculada, self._As_min)
        print(f"Armadura Adotada:\nAs+: {self.__As_adotada:.2f} cm2/m\tAs-: {self.__Ase_adotada:.2f} cm2/m\tAs sec: {self.__As_secundaria:.2f} cm2/m")
        return round(self.__As_calculada, 2), round(self.__Ase_calculada, 2), round(self._As_min, 2), round(self._Ase_min_bidirecional, 2), round(self.__As_secundaria, 2), round(self.__As_adotada, 2),round(self.__Ase_adotada, 2), round(self.__As_secundaria, 2)

    def detalhar_armaduras(self):
        lista = [[],[],[]]
        if self.__As_adotada > 0:
            print("Armadura Positiva Principal (As+):")
            for arranjo in self.detalhamento_armaduras(self.__As_adotada, self._ly, self._lx):
                lista[0].append(arranjo)
        if self.__Ase_adotada > 0:
            lista.append("As Negativa (As-):")
            for arranjo in self.detalhamento_armaduras(self.__Ase_adotada, self._ly, self._lx):
                lista[1].append(arranjo)
        if self.__As_secundaria > 0:
            print("As Secundária:")
            for arranjo in self.detalhamento_armaduras(self.__As_secundaria, self._lx, self._ly):
                lista[2].append(arranjo)
        return lista

    def calcular_flecha_inicial(self):
        print("Calculo da flecha inicial")
        if self._tipo_laje == 1:
            self.__k = 5
        elif self._tipo_laje == 2:
            self.__k = 2
        elif self._tipo_laje == 3:
            self.__k = 1
        elif self._tipo_laje == 4:
            self.__k = 48
            self._wlim = min(self._lx, self._ly) / 125
        else:
            print("Tipo de laje não encontrada")
        self._w0 = self.__k * self._p_serv * self._lx ** 4 / (384 * self._D)
        return round(self._w0*100,4)

class LajeBidirecional(Laje):
    def __init__(self, lx: float, ly: float, h: int, g: float, q: float, tipo_laje: int, concreto: Concreto, aco:Aco, bitolas, psi2=0.4):
        super().__init__(lx, ly, h, g, q, tipo_laje, concreto, aco, bitolas, psi2)

        self.__lambda, self.__wc, self.__mxe, self.__mye,self.__mx, self.__my, self.__mxy, self.__rxe, self.__rx, self.__rye, self.__ry, self.__beta_x, self.__beta_y = 0,0,0,0,0,0,0,0,0,0,0,0,0
        self.__mx,self.__mxe,self.__my,self.__mye = 0,0,0,0
        self.__Rx, self.__Rxe, self.__Ry, self.__Rye = 0, 0, 0, 0  # reações de apoio
        self.__Mx, self.__Mxe, self.__My, self.__Mye = 0, 0, 0, 0  # momentos
        self.__Asx_calculada, self.__Asxe_calculada, self.__Asy_calculada, self.__Asye_calculada = 0,0,0,0
        self.__As_minima_positiva, self.__As_minima_negativa = 0, 0
        self.__Asx_adotada, self.__Asxe_adotada, self.__Asy_adotada, self.__Asye_adotada = 0, 0, 0, 0


    def calcular_reacoes(self):
        lx_ly = self._lx / self._ly
        ly_lx = self._ly / self._lx
        if self._tipo_laje == 1:
            teste = buscar_parametros_laje (self, lx_ly, tabela_tipo1_lxly)
            print(teste)
        elif self._tipo_laje == 2:
            teste = buscar_parametros_laje(self, lx_ly, tabela_tipo2_lxly)
            print(teste)
        elif self._tipo_laje == 3:
            teste = buscar_parametros_laje(self, lx_ly, tabela_tipo3_lxly)
            print(teste)
        elif self._tipo_laje == 4:
            teste = buscar_parametros_laje(self, lx_ly, tabela_tipo4_lxly)
            print(teste)
        elif self._tipo_laje == 5:
            teste = buscar_parametros_laje(self, lx_ly, tabela_tipo5_lxly)
            print(teste)
        elif self._tipo_laje == 6:
            teste = buscar_parametros_laje(self, lx_ly, tabela_tipo6_lxly)
            print(teste)
        else:
            raise ValueError("Tipo de laje inválido. Escolha um número de 1 a 6.")

        self.__lambda, self.__wc, self.__mxe, self.__mye, self.__mx, self.__my, self.__mxy, self.__rxe, self.__rx, self.__rye, self.__ry, self.__beta_x, self.__beta_y = teste.values()
        return self.__lambda, self.__wc, self.__mxe, self.__mye, self.__mx, self.__my, self.__mxy, self.__rxe, self.__rx, self.__rye, self.__ry, self.__beta_x, self.__beta_y

    def calcular_reacoes_apoio(self):
        self.__Rx = 0.001 * self.__rx * self._p * self._lx
        self.__Rxe = 0.001 * self.__rxe * self._p * self._lx
        self.__Ry = 0.001 * self.__ry * self._p * self._lx
        self.__Rye = 0.001 * self.__rye * self._p * self._lx
        print(
            f"Reações de Apoio:\nRx: {self.__Rx:.2f}\tRxe: {self.__Rxe:.2f}\tRy: {self.__Ry:.2f}\tRye: {self.__Rye:.2f}")
        return round(self.__Rx,2), round(self.__Rxe,2), round(self.__Ry,2), round(self.__Rye,2)

    def calcular_momentos_fletores(self):
        self.__Mx = 0.001 * self.__mx * self._p * self._lx * self._lx
        self.__Mxe = 0.001 * self.__mxe * self._p * self._lx * self._lx
        self.__My = 0.001 * self.__my * self._p * self._lx * self._lx
        self.__Mye = 0.001 * self.__mye * self._p * self._lx * self._lx
        print(
            f"Momentos Fletores:\nMx: {self.__Mx:.2f}\tMxe: {self.__Mxe:.2f}\tRy: {self.__My:.2f}\tRye: {self.__Mye:.2f}")
        return round(self.__Mx,2), round(self.__Mxe,2),round(self.__My,2), round(self.__Mye,2)

    def calcular_armaduras(self):
        self.__Asx_calculada = self.calcular_As(self.__Mx)
        self.__Asxe_calculada = self.calcular_As(abs(self.__Mxe))
        self.__Asy_calculada = self.calcular_As(self.__My)
        self.__Asye_calculada = self.calcular_As(abs(self.__Mye))
        print(f"Armaduras Calculadas:\nAs x: {self.__Asx_calculada:.2f}\tAs xe: {self.__Asxe_calculada:.2f}\tAs y: {self.__Asy_calculada:.2f}\tAs ye: {self.__Asye_calculada:.2f}")
        self.__As_minima_positiva = self._As_min *.67
        self.__As_minima_negativa = self._As_min
        print(f"Armaduras Mínimas:\nAs+_min: {self.__As_minima_positiva:.2f}\tAs-_min: {self.__As_minima_negativa:.2f}")
        self.__Asx_adotada = max(self.__Asx_calculada, self.__As_minima_positiva)
        if self.__Mxe != 0:
            self.__Asxe_adotada = max(self.__Asxe_calculada, self.__As_minima_negativa)
        self.__Asy_adotada = max(self.__Asy_calculada, self.__As_minima_positiva)
        if self.__Mye != 0:
            self.__Asye_adotada = max(self.__Asye_calculada, self.__As_minima_negativa)
        print(
            f"Armaduras Adotadas:\nAs_x: {self.__Asx_adotada:.2f}\tAs_xe: {self.__Asxe_adotada:.2f}\tAs_y: {self.__Asy_adotada:.2f}\tAs_ye: {self.__Asye_adotada:.2f}")
        return round(self.__Asx_calculada,2), round(self.__Asxe_calculada,2),round(self.__Asy_calculada,2), round(self.__Asye_calculada,2),round(self.__As_minima_positiva,2), round(self.__As_minima_negativa,2),round(self.__As_minima_positiva,2), round(self.__As_minima_negativa,2),round(self.__Asx_adotada,2), round(self.__Asxe_adotada,2),round(self.__Asy_adotada,2), round(self.__Asye_adotada,2)

    def imprimir_parametros(self):
        print(f"{self.__lambda, self.__wc, self.__mxe, self.__mye,self.__mx, self.__my, self.__mxy, self.__rxe, self.__rx, self.__rye, self.__ry, self.__beta_x, self.__beta_y}")

    def calcular_flecha_inicial(self):
        self._w0 = 0.001 * self.__wc * self._p_serv * self._lx ** 4 / (self._D)
        return round(self._w0*100,4)

    def detalhar_armaduras(self):
        lista = [[], [], [], []]
        if self.__Asx_adotada > 0:
            print(f"Armadura Positiva X (Asx+):{self.__Asx_adotada}")
            for arranjo in self.detalhamento_armaduras(self.__Asx_adotada, self._ly, self._lx):
                lista[0].append(arranjo)
            print(f"Lista 00 :{lista[0]}")
        if self.__Asxe_adotada > 0:
            print(f"As Negativa X (Asx-): {self.__Asxe_adotada}")
            for arranjo in self.detalhamento_armaduras(self.__Asxe_adotada, self._ly, self._lx):
                lista[1].append(arranjo)
            print(f"Lista 01 :{lista[1]}")
        if self.__Asy_adotada > 0:
            print(f"Armadura Positiva Y (Asy+): {self.__Asy_adotada}")
            for arranjo in self.detalhamento_armaduras(self.__Asy_adotada, self._lx, self._ly):
                lista[2].append(arranjo)
            print(f"Lista 02 :{lista[2]}")
        if self.__Asye_adotada > 0:
            print(f"As Negativa Y (Asy-): {self.__Asye_adotada}")
            for arranjo in self.detalhamento_armaduras(self.__Asye_adotada, self._lx, self._ly):
                lista[3].append(arranjo)
            print(f"Lista 03 :{lista[3]}")
        print("Fim DETALHAR ARMADURAS BIDIRECIONAIS")
        return lista

class LajeLisa(Laje):
    def __init__(self, h, concreto, Ai, qmedio, C1, C2, tipo_pilar):
        super().__init__(
            lx=0,                     # valor neutro
            ly=0,                     # valor neutro
            h=h,
            g=0,                      # carga permanente irrelevante aqui
            q=0,                      # carga acidental irrelevante aqui
            tipo_laje=0,             # ou algum código padrão para "Lisa"
            concreto=concreto,
            aco=None,                # sem aço neste modelo
            bitolas=None,            # idem
            psi2=0.4,
            cobrimento=3.0
        )
        #self.h = h  # altura da laje em cm
        #self.concreto = concreto  # objeto da classe Concreto
        self.Ai = Ai  # área de influência (m²)
        self.qmedio = qmedio  # carga média (kN/m²)
        self.C1 = C1 # lado 1 do pilar (m)
        self.C2 = C2 # lado 2 do pilar (m)
        self.tipo_pilar = tipo_pilar  # enum TipoPilarEnum

    def calcular_puncao(self):
        # Cálculo das taxas mínimas de armaduras
        #ro_x = 2*(self._ro_min *((6*self._d+self.C2)*self._h))
        ro_x = self._ro_min # armadura mínima negativa (somente a armadura tracionada)
        ro_y = self._ro_min # armadura mínima negativa (somente a armadura tracionada)
        ro = np.sqrt(ro_x*ro_y)

        tal_Rd1 =(0.13*(1 + np.sqrt(20 / self._d))*np.pow(100 * ro * self._concreto.fck, 1 / 3))/10 #kN/m2
        print(f"d: {self._d}")
        print(f"ro: {ro}")
        # Perímetro de controle (simplificação para pilar retangular)
        if self.tipo_pilar.value == "interior":
            u0 = 2 * (self.C1 + self.C2)
            u = (2*(self.C1 + self.C2))+ (4 * np.pi*self._d)
        elif self.tipo_pilar.value == "borda":
            a0 = min(1.5*self._d,self.C1/2)
            u0 = (2*a0) + self.C2
            print(f"a0: {a0}")
            u = 2*a0 + self.C2 + (2*np.pi*self._d)
        elif self.tipo_pilar.value == "canto":
            a1 = min(1.5*self._d,self.C1/2)
            a2 = min(1.5*self._d,self.C2/2)
            u0 = a1 + a2
            u = a1 + a2 + np.pi*self._d
            print(f"a1: {a1}")
            print(f"a2: {a2}")
        else:
            raise ValueError("Tipo de pilar inválido.")
        print(f"u0: {u0}")
        print(f"u: {u}")
        # Tensão de cálculo
        P = self.Ai * self.qmedio # kN
        print(f"P: {P}")
        tal_Sd_concreto = P/(u0*self._d) # Tensão Solicitante em kN/m²
        # Resistência de punção simplificada (fórmula da NBR 6118)
        print(f"TalSd concreto: {tal_Sd_concreto}")
        tal_Sd_aco = P / (u * self._d)  # Tensão Solicitante em kN/m²
        tal_Rd2 = self._concreto.tal_Rd2
        print(f"TalRd2: {tal_Rd2}")
        print(f"TalRd1: {tal_Rd1}")
        return {
            # verificação do esmagamento da diagonal comprimida
            "tensao_calc": round(tal_Sd_concreto, 2),
            "resistencia_puncao": round(tal_Rd2, 2),
            "verificado": tal_Sd_concreto <= tal_Rd2,
            # verificação da necessidade de armaduras (pinos)
            "v_solicitante": round(tal_Sd_aco, 2),
            "v_resistente": round(tal_Rd1 , 2),
            "verificado_pinos": tal_Sd_concreto <= tal_Rd1
        }


