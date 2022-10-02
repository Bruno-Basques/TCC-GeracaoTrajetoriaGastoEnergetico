def tempo_transicao_parabolico_linear(temp_tot_mov, acel_const, posi_n_fina, posi_n_inic):
    """
    A função "tempo_transicao_parabolico_linear" tem como entrada o tempo total de movimento,
    a aceleração constante do seguimento parabôlico, bem como a posição inicial e final, sendo retornado o tempo em que
    ocorre a transição do seguimento parabólico para o linear.
    Variáveis:
    temp_tot_mov = tempo total do seguimento da trajetória, em segundos;
    acel_const = aceleração constante do seguimento parabólico, em radianos/s²;
    posi_n_fina = posição final de theta para o seguimento em questão, em radianos;
    posi_n_inic = posição inicial de theta para o seguimento em questão, em radianos;
    temp_parab_linea = tempo em que ocorre a transição do seguimento parabólico para o linear, em segundos;
    """
    fragmentacao = ((acel_const ** 2 * temp_tot_mov ** 2) - (4 * acel_const * (posi_n_fina - posi_n_inic)))
    if fragmentacao < 1 * 10 ** -15:
        fragmentacao = 0
    temp_parab_linea = (temp_tot_mov / 2) - (fragmentacao ** 0.5) / (2 * acel_const)
    return temp_parab_linea


# Trajetoria linear
def trajetoria_linear_simples(temp_tot_mov, posi_n_inic, posi_n_fina, acel_const):
    """
    A função "trajetoria_linear_simples" tem como entrada o tempo total de movimento,
    a aceleração constante do seguimento parabôlico, bem como a posição inicial e final,
    sendo retornado as posições que a junta n assume em uma determinada trajetória,
    regida por uma função linear com extremidades parabólicas.
    Variáveis:
    temp_tot_mov = tempo total de duração do movimento, em segundos;
    acel_const = aceleração constante da região parabólica da função da trajetória, em radianos/s²;
    posi_n_inic = posição inicial da junta n, em radianos;
    posi_n_fina = posição final da junta n, em radianos;
    lista_posicoes = lista contendo todas as posições calculadas dentro do intervalo e com delta t determinados;
    temp_parab_linea = tempo em que ocorre a transição da função parabólica para a linear, em segundos;
    posi_n_line_inic = posição da junta n em que ocorre a transição da função parabólica para a linear, em radianos;
    posi_n_line_fina = posição da junta n em que ocorre a transição da função linear para a parabólica, em radianos;
    posi_n_meta_traj = posição da junta n em que se chega na metade da trajetória, em radianos;
    delta_t = fração de tempo utilizada para se discretizar as integrais dos calculos;
    """
    lista_posicoes = list()
    contador2 = 0
    temp_parab_linea = tempo_transicao_parabolico_linear(temp_tot_mov, acel_const, posi_n_fina, posi_n_inic)
    veloc_h = temp_parab_linea * acel_const
    while contador2 < temp_tot_mov:
        if contador2.__le__(round(temp_parab_linea)):
            lista_posicoes.append(posi_n_inic + 0.5 * acel_const * contador2 ** 2)
        elif contador2 > temp_parab_linea and contador2.__le__(int(temp_tot_mov - temp_parab_linea)):
            lista_posicoes.append(lista_posicoes[int(temp_parab_linea)] + veloc_h * (contador2 - temp_parab_linea))
        else:
            lista_posicoes.append(posi_n_fina - 0.5 * acel_const * (temp_tot_mov - contador2) ** 2)
        contador2 += 1

    return lista_posicoes
