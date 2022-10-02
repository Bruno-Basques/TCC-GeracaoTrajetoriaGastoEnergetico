from math import pi


class Elo:

    def __init__(self, densidade, diametro, comprimento):
        self.__densidade = densidade
        self.__massa = densidade * (comprimento * pi * (diametro / 2) ** 2)
        self.__diamentro = diametro
        self.__comprimento = comprimento
        self.__inercia = ((self.__massa / 4) * (diametro ** 2) / 4) + ((self.__massa / 3) * comprimento ** 2)

    def densidade(self):
        return self.__densidade

    def massa(self):
        return self.__massa

    def diametro(self):
        return self.__diamentro

    def comprimento(self):
        return self.__comprimento

    def inercia(self):
        return self.__inercia
