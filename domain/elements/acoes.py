class Acoes:
    def __init__(self: object, NSk: float = 0, MSkx: float = 0, MSky: float = 0, VSk: float = 0, gama_F = 1.4) -> None:
        self.__NSk = NSk
        self.__MSkx = MSkx
        self.__MSky = MSky
        self.__VSk = VSk
        self.__gama_F = gama_F
        # Adimensionais
        self.__NSd, self.__MSdx, self.__MSdy, self.__VSd = self.majorar_esforcos()

    @property
    def Aw(self):
        return self.__Aw

    @property
    def NSd(self):
        return self.__NSd

    @property
    def MSdx(self):
        return self.__MSdx

    @property
    def MSdy(self):
        return self.__MSdy

    @property
    def VSd(self):
        return self.__VSd

    def majorar_esforcos(self):
        return (self.__NSk * self.__gama_F, self.__MSkx * self.__gama_F, self.__MSky * self.__gama_F, self.__VSk * self.__gama_F)