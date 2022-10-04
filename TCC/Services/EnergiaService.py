def energia_elo_i(tempo_discretizacao_somatorio, list_torq_gera_i, motor_constante_torque, motor_resistencia_armadura,
                 motor_indutancia_armadura, motor_constante_proporcionalidade_tensao_velocidade, infinitesimal_discretizacao,
                 lista_velocidades_angulares_theta_i):
    """
    A função "energia_elo_i" calcula a energia gasta para movimentar o elo i.
    Variáveis:
    tempo_discretizacao_somatorio = Tempo utilizado para discretizar uma integral em um somatório, em ms;
    list_torq_gera_i = Lista de torques eletromagnéticos líquidos performado pelo motor i, em N*m;
    motor_constante_torque = Constante de torque do motor, em N.m/A;
    motor_resistencia_armadura = Resistência elétrica da armadura do motor, em ohm;
    motor_indutancia_armadura = Indutância elétrica da armadura do motor, em H;
    motor_constante_proporcionalidade_tensao_velocidade = Constante de proporcionalidade entre a tensão aplicada e a
                                                          velocidade de rotação do motor;
    infinitesimal_discretizacao = Infinitezimal de tempo utilizado para discretizar uma integral em um somatório, em s;
    lista_velocidades_angulares_theta_i = Lista de velocidades angulares para a junta i;


    corr_arma_i = Corrente elétrica que percorre a armadura do motor 1, em A;
    list_corrent_i = Lista com as correntes elétricas da armadura para cada instante discretizado do tempo;
    tens_arma = Tensão aplicada no motor, em V;
    ener_movi_i = Energia consumida pelo motor 1 para realizar o movimento proposto do manipulador planar de 2 GDL, em J;
    Em que i = (1 ou 2);
    """
    list_corrent_i = list()
    corr_arma_i = 0
    ener_movi_i = 0

    for c in range(tempo_discretizacao_somatorio):
        corr_arma_i = list_torq_gera_i[c] / motor_constante_torque
        list_corrent_i.append(corr_arma_i)

    for b in range(tempo_discretizacao_somatorio - 1):
        tens_arma = motor_resistencia_armadura * corr_arma_i + motor_indutancia_armadura * abs(
            (list_corrent_i[b + 1] - list_corrent_i[b]) / infinitesimal_discretizacao) + \
                    motor_constante_proporcionalidade_tensao_velocidade * abs(lista_velocidades_angulares_theta_i[b])
        ener_movi_i += abs(tens_arma * list_corrent_i[b] * infinitesimal_discretizacao)

    return ener_movi_i

