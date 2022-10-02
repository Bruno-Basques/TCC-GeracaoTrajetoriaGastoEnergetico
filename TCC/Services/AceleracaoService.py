def aceleracao_angular(posi_n_inic, posi_n_fina, temp_tot_mov):
    """
    A função "aceleracao_angular" tem como entrada a posição inicial, final e o tempo de movimento, sendo retornado
    a aceleração angular resultante.
    Variáveis:
    temp_tot_mov = tempo total de duração do movimento, em segundos;
    acel_const = aceleração angular, em radianos/s²;
    posi_n_inic = posição inicial da junta n, em radianos;
    posi_n_fina = posição final da junta n, em radianos;
    """
    acel_const = 4 * (posi_n_fina - posi_n_inic) / (temp_tot_mov ** 2)
    return acel_const


def aceleracao_linear(posi_n_inic, posi_n_fina, temp_tot_mov):
    """
    A função "aceleracao_linear" tem como entrada a posição inicial, final e o tempo de movimento, sendo retornado
    a aceleração linear.
    Variáveis:
    temp_tot_mov = tempo total de duração do movimento, em segundos;
    acel_const = aceleração constante da região parabólica da função da trajetória, em m/s²;
    posi_n_inic = posição inicial da junta n, em m;
    posi_n_fina = posição final da junta n, em m;
    """
    acel_const = 4 * (posi_n_fina - posi_n_inic) / (temp_tot_mov ** 2)
    return acel_const
