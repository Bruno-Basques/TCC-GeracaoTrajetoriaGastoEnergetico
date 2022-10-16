from math import pi


def conversao_grau_radiano(angulo_grau):
    """
    A função "conversao_grau_radiano" tem como entrada um ângulo em graus,
    sendo retornado esse ângulo em radianos.
    Variáveis:
    angulo_grau = ângulo que se quer converter, em graus;
    angulo_radiano = ângulo convertido, em radianos;
    """
    angulo_radiano = angulo_grau * (pi/180)
    return angulo_radiano


def conversao_radiano_grau(angulo_radiano):
    """
    A função "conversao_radiano_grau" tem como entrada um ângulo em radianos,
    sendo retornado esse ângulo em graus.
    Variáveis:
    angulo_radiano = ângulo que se quer converter, em radianos;
    angulo_grau = ângulo convertido, em graus;
    """
    angulo_grau = angulo_radiano * (180 / pi)
    return angulo_grau


