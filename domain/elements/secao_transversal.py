class SecaoRetangular:
    def __init__(self: object, hx: int = 2, hy: int = 2, lex: int = 300, ley: int = 300) -> None:
        self.__hx = hx
        self.__hy = hy
        self.__lex = lex
        self.__ley = ley
        # Adimensionais
        self.__Aw, self.__I_x, self.__I_y, self.__W_x, self.__W_y, self.__k_x, self.__k_y = self.calcular_prop_geom_retangular()
        self.__kx = (self.__I_x/self.__Aw)**0.5
        self.__ky = (self.__I_y / self.__Aw) ** 0.5
        self.__lambda_x = self.__lex / self.__kx
        self.__lambda_y = self.__ley / self.__ky

    @property
    def Aw(self):
        return self.__Aw

    @property
    def hx(self):
        return self.__hx
    @property
    def hy(self):
        return self.__hy

    @property
    def Ix(self):
        return self.__I_x
    @property
    def Iy(self):
        return self.__I_y

    @property
    def lambda_x(self):
        return self.__lambda_x

    @property
    def lambda_y(self):
        return self.__lambda_y

    def calcular_prop_geom_retangular(self):
        b = self.__hx
        h = self.__hy
        Aw = b * h
        # momento de inércia
        Ix = (b * h * h * h) / 12
        Iy = (h * b * b * b) / 12
        # módulo resistente
        Wx = Ix / (0.5 * h)
        Wy = Iy / (0.5 * b)
        # raios de giração
        kx = (Ix / Aw) ** 0.5
        ky = (Iy / Aw) ** 0.5

        return Aw, Ix, Iy, Wx, Wy, kx, ky

    """
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





    def resultados(self):
        return round(self.__Mdtotx,2), round(self.__Mdtoty,2) # self.__Mdtotx, self.__Mdtoty, self.__Mdtotx, self.__Mdtoty
"""









