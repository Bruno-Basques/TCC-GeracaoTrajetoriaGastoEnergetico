def velocidade_angular(thetn, thetn_mais_um, temp_dura_inte):
    """
    A função "velocidade_angular" tem como entrada a posição de uma junta n em um determinado momento e
    no momento imediatamente seguinte, bem como o tempo entre esses dois momentos, sendo retornado a velocidade angular
    dos trechos lineares da função da trajetória.
    Variáveis:
    thetn = theta n, em radianos;
    thetn_mais_um = theta n+1, em radianos;
    temp_dura_inte = tempo de duração do intervalo entre theta n e theta n+1, em segundos;
    velo_angu = velocidade angular, em radianos/s;
    """
    velo_angu = (thetn_mais_um - thetn) / temp_dura_inte
    return velo_angu