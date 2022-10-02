class Movimento:
    def __init__(self,
                 theta1_inicial,
                 theta1_final,
                 theta2_inicial,
                 theta2_final,
                 tempo_total,
                 infinitesimal):
        self.__theta1_inicial = theta1_inicial
        self.__theta1_final = theta1_final
        self.__theta2_inicial = theta2_inicial
        self.__theta2_final = theta2_final
        self.__tempo_total = tempo_total
        self.__infinitesimal = infinitesimal
        self.__tempo_somatorio = int(tempo_total / infinitesimal)

    def theta1_inicial(self):
        return self.__theta1_inicial

    def theta1_final(self):
        return self.__theta1_final

    def theta2_inicial(self):
        return self.__theta2_inicial

    def theta2_final(self):
        return self.__theta2_final

    def tempo_total(self):
        return self.__tempo_total

    def infinitesimal(self):
        return self.__infinitesimal

    def tempo_somatorio(self):
        return self.__tempo_somatorio
