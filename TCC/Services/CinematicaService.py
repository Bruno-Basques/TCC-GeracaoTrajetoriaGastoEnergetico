from math import atan2, cos, sin


def cinematica_direta_posicoes_x_y(junta_1, junta_2, compri_1, compri_2):
    """
    A função "cinematica_direta_posicoes_x_y" tem como entrada as posições das juntas de revolução e os comprimentos
    dos elos 1 e 2, sendo retornado os valores X e Y, que descrevem uma posição no plano cartesiano.
    Variáveis:
    junta_1 = Posição da junta de revolução 1, em radianos;
    junta_2 = Posição da junta de revolução 2, em radianos;
    compri_1 = Comprimento do elo 1, em metros;
    compri_2 = Comprimento do elo 2, em metros;
    posicao_x = Valor que descreve a posição transformada em relação ao eixo X, em metros;
    posicao_y = Valor que descreve a posição transformada em relação ao eixo Y, em metros;
    """
    posicao_x = compri_1 * cos(junta_1) + compri_2 * cos(junta_1 + junta_2)
    posicao_y = compri_1 * sin(junta_1) + compri_2 * sin(junta_1 + junta_2)
    return posicao_x, posicao_y


def cinematica_inversa_posicoes_junta_1e2(coord_x, coord_y, compri_1, compri_2):
    """
    A função "posicoes_junta_1e2" tem como entrada as coordenadas X e Y, de uma posição no plano cartesiano, e os
    comprimentos dos elos 1 e 2, sendo retornado os valores theta 1 e theta 2,
    que descrevem uma posição no plano das juntas.
    Variáveis:
    coord_x = coordenada x, em metros;
    coord_y = coordenada y, em metros;
    compri_1 = comprimento do braço 1, em metros;
    compri_2 = comprimento do braço 2, em metros;
    cos_thet2 = cosseno do ângulo theta 2;
    sen_thet2 = seno do ângulo theta 2;
    thet1 = theta 1, em radiano;
    thet2 = theta 2, em radiano;
    k1 = substituição na equação, para simplificação;
    k2 = substituição na equação, para simplificação;
    """
    cos_thet2 = (coord_x ** 2 + coord_y ** 2 - compri_1 ** 2 - compri_2 ** 2) / (2 * compri_1 * compri_2)
    if -1 < cos_thet2 < 1:
        sen_thet2 = ((1 - cos_thet2 ** 2) ** 0.5)
        thet2 = atan2(sen_thet2, cos_thet2)
        k1 = compri_1 + compri_2 * cos_thet2
        k2 = compri_2 * sen_thet2
        thet1 = atan2(coord_y, coord_x) - atan2(k2, k1)
        return thet1, thet2
    return print(f'As coordenadas ({coord_x}, {coord_y}) estão fora do espaço de trabalho do manipulador')
