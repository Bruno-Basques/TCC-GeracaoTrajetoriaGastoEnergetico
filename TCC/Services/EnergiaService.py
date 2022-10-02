def energia_elo1(tempo_discretizacao_somatorio,
                 list_torq_gera1, motor_constante_torque,
                 motor_resistencia_armadura,
                 motor_indutancia_armadura,
                 motor_constante_proporcionalidade_tensao_velocidade,
                 infinitesimal_discretizacao,
                 lista_velocidades_angulares_theta1):
    """
    A função "energia_elo1" calcula a energia gasta para movimentar o elo 1, considerando a inércia e
    outras propriedades do elo 2.
    Variáveis:
    tempo_discretizacao_somatorio = Tempo utilizado para discretizar uma integral em um somatório, em ms;
    lista_velocidades_angulares_thetai = Lista de velocidades angulares para a junta i (1 ou 2);
    motor_constante_torque = Constante de torque do motor, em N.m/A;
    motor_resistencia_armadura = Resistência elétrica da armadura do motor, em ohm;
    motor_indutancia_armadura = Indutância elétrica da armadura do motor, em H;
    infinitesimal_discretizacao = Infinitezimal de tempo utilizado para discretizar uma integral em um somatório, em s;
    motor_constante_proporcionalidade_tensao_velocidade = Constante de proporcionalidade entre a tensão aplicada e a
                                                          velocidade de rotação do motor;
    torq_1 = Torque necessário para movimentar o conjunto dos elos 1 e 2, em N*m;
    list_torq_gera1 = Lista de torques eletromagnéticos líquidos performado pelo motor 1, em N*m;
    corr_arma1 = Corrente elétrica que percorre a armadura do motor 1, em A;
    list_corrent1 = Lista com as correntes elétricas da armadura para cada instante discretizado do tempo;
    tens_arma = Tensão aplicada no motor, em V;
    ener_movi1 = Energia consumida pelo motor 1 para realizar o movimento proposto do manipulador planar de 2 GDL, em J;
    """
    list_corrent1 = list()
    corr_arma1 = 0
    ener_movi1 = 0

    for c in range(tempo_discretizacao_somatorio):
        corr_arma1 = list_torq_gera1[c] / motor_constante_torque
        list_corrent1.append(corr_arma1)

    for b in range(tempo_discretizacao_somatorio - 1):
        tens_arma = motor_resistencia_armadura * corr_arma1 + motor_indutancia_armadura * abs(
            (list_corrent1[b + 1] - list_corrent1[b]) / infinitesimal_discretizacao) + \
                    motor_constante_proporcionalidade_tensao_velocidade * abs(lista_velocidades_angulares_theta1[b])
        ener_movi1 += abs(tens_arma * list_corrent1[b] * infinitesimal_discretizacao)

    return ener_movi1


def energia_elo2(tempo_discretizacao_somatorio,
                 list_torq_gera2, motor_constante_torque,
                 motor_resistencia_armadura,
                 motor_indutancia_armadura,
                 motor_constante_proporcionalidade_tensao_velocidade,
                 infinitesimal_discretizacao,
                 lista_velocidades_angulares_theta2):

    list_corrent2 = list()
    corr_arma2 = 0
    ener_movi2 = 0

    for e in range(tempo_discretizacao_somatorio):
        corr_arma2 = list_torq_gera2[e] / motor_constante_torque
        list_corrent2.append(corr_arma2)

    for d in range(tempo_discretizacao_somatorio - 1):
        tens_arma2 = motor_resistencia_armadura * corr_arma2 + motor_indutancia_armadura * abs(
            (list_corrent2[d + 1] - list_corrent2[d]) / infinitesimal_discretizacao) + \
                     motor_constante_proporcionalidade_tensao_velocidade * abs(lista_velocidades_angulares_theta2[d])
        ener_movi2 += abs(tens_arma2 * list_corrent2[d] * infinitesimal_discretizacao)
    return ener_movi2
