class Motor:

    def __init__(self,
                 resistencia_armadura,
                 indutancia_armadura,
                 momento_inercia_motor,
                 torque_atrito,
                 coeficiente_atrito_viscoso,
                 constante_proporcionalidade_tensao_velocidade,
                 constante_torque_motor):
        self.__resistencia_armadura = resistencia_armadura
        self.__indutancia_armadura = indutancia_armadura
        self.__momento_inercia_motor = momento_inercia_motor
        self.__torque_atrito = torque_atrito
        self.__coeficiente_atrito_viscoso = coeficiente_atrito_viscoso
        self.__constante_proporcionalidade_tensao_velocidade = constante_proporcionalidade_tensao_velocidade
        self.__constante_torque_motor = constante_torque_motor

    def resistencia_armadura(self):
        return self.__resistencia_armadura

    def indutancia_armadura(self):
        return self.__indutancia_armadura

    def momento_inercia_motor(self):
        return self.__momento_inercia_motor

    def torque_atrito(self):
        return self.__torque_atrito

    def coeficiente_atrito_viscoso(self):
        return self.__coeficiente_atrito_viscoso

    def constante_proporcionalidade_tensao_velocidade(self):
        return self.__constante_proporcionalidade_tensao_velocidade

    def constante_torque_motor(self):
        return self.__constante_torque_motor
