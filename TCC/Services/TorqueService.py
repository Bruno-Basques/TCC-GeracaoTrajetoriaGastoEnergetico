from math import cos, sin


def calculo_torque_elo1(tempo_discretizacao_somatorio, elo1_inercia, elo1_massa, elo1_comprimento, elo2_inercia, elo2_massa,
                        elo2_comprimento, lista_pontos_interm_espaco_juntas1, lista_pontos_interm_espaco_juntas2,
                        lista_aceleracoes_angulares_theta1, lista_aceleracoes_angulares_theta2, lista_velocidades_angulares_theta1,
                        lista_velocidades_angulares_theta2, motor_torque_atrito, motor_momento_inercia,
                        motor_coeficiente_atrito_viscoso):
    """
    A função "calculo_torque_elo1" calcula o torque necessário para movimentar o elo 1, considerando a inércia e
    outras propriedades do elo 2.
    Variáveis:
    tempo_discretizacao_somatorio = Tempo utilizado para discretizar uma integral em um somatório, em ms;
    eloi_inercia = Inércia do elo i (1 ou 2), em N*m;;
    eloi_massa = Massa do elo i (1 ou 2), em kg;
    eloi_comprimento = Comprimento do elo i (1 ou 2), em metros;
    lista_pontos_interm_espaco_juntasi = Lista de pontos da trajetória no espaço das juntas para a junta i (1 ou 2);
    lista_aceleracoes_angulares_thetai = Lista de acelerações angulares para a junta i (1 ou 2);
    lista_velocidades_angulares_thetai = Lista de velocidades angulares para a junta i (1 ou 2);
    motor_torque_atrito = Torque gerado pelo atrito interno do motor, em N*m;
    motor_momento_inercia = Momento de inércia do motor, em kg*m²;
    motor_coeficiente_atrito_viscoso = Coeficiente de atrito viscoso do motor, em kg*m²/s;
    torq_1 = Torque necessário para movimentar o conjunto dos elos 1 e 2, em N*m;
    torq_gera1 = Torque eletromagnético líquido performado pelo motor 1, em N*m;
    """
    aceleracao_gravidade = 9.81
    list_torq_gera1 = list()
    for a in range(tempo_discretizacao_somatorio):
        torq_1 = (elo1_inercia + elo2_inercia + 0.25 * (
                elo1_massa * elo1_comprimento ** 2 + elo2_massa * elo2_comprimento ** 2) +
                  elo2_massa * elo1_comprimento ** 2 + elo2_massa * elo1_comprimento * elo2_comprimento * cos(
                    lista_pontos_interm_espaco_juntas2[a])) * lista_aceleracoes_angulares_theta1[a] + (
                         elo2_inercia + 0.25 * elo2_massa * elo2_comprimento ** 2 +
                         0.5 * elo2_massa * elo1_comprimento * elo2_comprimento * cos(
                           lista_pontos_interm_espaco_juntas2[a])) * lista_aceleracoes_angulares_theta2[
                     a] - 0.5 * elo2_massa * elo1_comprimento * elo2_comprimento * sin(
            lista_pontos_interm_espaco_juntas2[a]) * lista_velocidades_angulares_theta2[
                     a] ** 2 - elo2_massa * elo1_comprimento * elo2_comprimento * sin(
            lista_pontos_interm_espaco_juntas2[a]) * lista_velocidades_angulares_theta1[a] * \
                 lista_velocidades_angulares_theta2[a] + (0.5 * elo2_massa * elo2_comprimento * cos(
                   lista_pontos_interm_espaco_juntas1[a] + lista_pontos_interm_espaco_juntas2[a]) +
                                                          elo1_comprimento * (0.5 * elo1_massa + elo2_massa) * cos(
                    lista_pontos_interm_espaco_juntas1[a])) * aceleracao_gravidade

        torq_gera1 = motor_torque_atrito + abs(torq_1) + motor_momento_inercia * abs(lista_aceleracoes_angulares_theta1[a]) + \
            motor_coeficiente_atrito_viscoso * abs(lista_velocidades_angulares_theta1[a])
        list_torq_gera1.append(torq_gera1)
    return list_torq_gera1


def calculo_torque_elo2(tempo_discretizacao_somatorio, elo1_comprimento, elo2_inercia, elo2_massa, elo2_comprimento,
                        lista_pontos_interm_espaco_juntas1, lista_pontos_interm_espaco_juntas2, lista_aceleracoes_angulares_theta1,
                        lista_aceleracoes_angulares_theta2, lista_velocidades_angulares_theta2, motor_torque_atrito,
                        motor_momento_inercia, motor_coeficiente_atrito_viscoso):
    """
    A função "calculo_torque_e_energia_elo2" calcula a energia gasta para movimentar o elo 2.
    Variáveis:
    tempo_discretizacao_somatorio = Tempo utilizado para discretizar uma integral em um somatório, em ms;
    eloi_inercia = Inércia do elo 2, em N*m;;
    eloi_massa = Massa do elo 2, em kg;
    eloi_comprimento = Comprimento do elo i (1 ou 2), em metros;
    lista_pontos_interm_espaco_juntasi = Lista de pontos da trajetória no espaço das juntas para a junta i (1 ou 2);
    lista_aceleracoes_angulares_thetai = Lista de acelerações angulares para a junta i (1 ou 2);
    lista_velocidades_angulares_thetai = Lista de velocidades angulares para a junta i (1 ou 2);
    motor_torque_atrito = Torque gerado pelo atrito interno do motor, em N*m;
    motor_momento_inercia = Momento de inércia do motor, em kg*m²;
    motor_coeficiente_atrito_viscoso = Coeficiente de atrito viscoso do motor, em kg*m²/s;
    torq_2 = Torque necessário para movimentar o elo 2;
    torq_gera2 = Torque eletromagnético líquido performado pelo motor 2, em N*m;
    corr_arma2 = Corrente elétrica que percorre a armadura do motor 2, em A;
    list_corrent2 = Lista com as correntes elétricas da armadura para cada instante discretizado do tempo;
    tens_arma = Tensão aplicada no motor, em V;
    ener_movi2 = Energia consumida pelo motor 2 para realizar o movimento proposto do manipulador planar de 2 GDL, em J;
    """
    list_torq_gera2 = list()
    aceleracao_gravidade = 9.81

    for c in range(tempo_discretizacao_somatorio):
        torq_2 = (elo2_inercia + 0.25 * elo2_massa * elo2_comprimento ** 2 +
                  0.5 * elo2_massa * elo1_comprimento * elo2_comprimento * cos(
                    lista_pontos_interm_espaco_juntas2[c])) * lista_aceleracoes_angulares_theta1[c] + \
                 (elo2_inercia + 0.25 * elo2_massa * elo2_comprimento ** 2) * lista_aceleracoes_angulares_theta2[c] \
                 + 0.5 * elo2_massa * elo1_comprimento * elo2_comprimento * sin(lista_pontos_interm_espaco_juntas2[c]) \
                 * lista_pontos_interm_espaco_juntas1[c] ** 2 + 0.5 * elo2_massa * elo2_comprimento * \
                 cos(lista_pontos_interm_espaco_juntas1[c] + lista_pontos_interm_espaco_juntas2[c]) * \
                 aceleracao_gravidade

        torq_gera2 = motor_torque_atrito + abs(torq_2) + motor_momento_inercia * abs(lista_aceleracoes_angulares_theta2[
            c]) + motor_coeficiente_atrito_viscoso * abs(lista_velocidades_angulares_theta2[c])
        list_torq_gera2.append(torq_gera2)
    return list_torq_gera2
