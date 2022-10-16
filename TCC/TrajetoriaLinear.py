from math import pi
from Model.EloModel import Elo
from Model.MotorModel import Motor
from Model.MovimentoModel import Movimento
from Services.AceleracaoService import aceleracao_linear
from Services.CinematicaService import cinematica_inversa_posicoes_junta_1e2, cinematica_direta_posicoes_x_y
from Services.EnergiaService import energia_elo_i
from Services.GraficoService import criar_grafico
from Services.TorqueService import calculo_torque_elo1, calculo_torque_elo2
from Services.TrajetoriaService import trajetoria_linear_simples
from Services.VelocidadeService import velocidade_angular
from TCC.Services.ConversaoUnidadesService import conversao_grau_radiano, conversao_radiano_grau

# Criação dos objetos motor, elos (1 e 2) e movimento.

motor = Motor(1, 0.046, 0.093, 0, 0.008, 0.55, 0.55)
elo1 = Elo(2700, 0.05, 0.5)
elo2 = Elo(2700, 0.05, 0.5)
trajetoria = Movimento(conversao_grau_radiano(15), conversao_grau_radiano(105),
                       conversao_grau_radiano(60), conversao_grau_radiano(60), 10, 0.001)

# Início do cálculo da energia gasta para movimentar o planar de dois graus de liberdade com a junta 2 móvel.

# Declaração dos valores iniciais e finais de X e Y no plano cartesiano para a trajetória com a junta 2 móvel.
parametro_x_inicial = 0.612372435696
parametro_x_final = -0.612372435696
parametro_y = 0.612372435696
acel_cartesiana = aceleracao_linear(parametro_x_inicial, parametro_x_final, trajetoria.tempo_somatorio())

# Criando uma lista com os pontos, no plano cartesiano, que formam o trajeto linear do braço planar.
pontos_interm_espaco_cartesiano = trajetoria_linear_simples(trajetoria.tempo_somatorio(), parametro_x_inicial,
                                                            parametro_x_final, acel_cartesiana)
pontos_interm_espaco_junta1 = list()
pontos_interm_espaco_junta2 = list()
tempo_thet_thet_mais1 = list()

h = 0
while h < trajetoria.tempo_somatorio():
    # Criando uma lista com os pontos do espaço das juntas a partir de coordenadas do eixo cartesiano
    theta1, theta2 = cinematica_inversa_posicoes_junta_1e2(pontos_interm_espaco_cartesiano[h], parametro_y,
                                                           elo1.comprimento(), elo2.comprimento())
    pontos_interm_espaco_junta1.append(theta1)
    pontos_interm_espaco_junta2.append(theta2)

    if(h == 5351):
        print("cu")
    h += 1

velocidades_angulares_theta1 = list()
velocidades_angulares_theta1.append(0)  # Velocidade inicial é 0

velocidades_angulares_theta2 = list()
velocidades_angulares_theta2.append(0)  # Velocidade inicial é 0

i = 0
while i < trajetoria.tempo_somatorio() - 2:
    # Adicionando as velocidades calculadas ponto a ponto da junta 1
    velocidades_angulares_theta1.append(velocidade_angular(pontos_interm_espaco_junta1[i],
                                                           pontos_interm_espaco_junta1[i + 1],
                                                           trajetoria.infinitesimal()))

    # Adicionando as velocidades calculadas ponto a ponto da junta 2
    velocidades_angulares_theta2.append(velocidade_angular(pontos_interm_espaco_junta2[i],
                                                           pontos_interm_espaco_junta2[i + 1],
                                                           trajetoria.infinitesimal()))

    i += 1

velocidades_angulares_theta1.append(0)  # Velocidade final é 0
velocidades_angulares_theta2.append(0)

aceleracoes_angulares_theta1 = list()
aceleracoes_angulares_theta2 = list()

aceleracoes_angulares_theta1.append(0)  # Aceleração inicial é 0
aceleracoes_angulares_theta2.append(0)

j = 0
while j < trajetoria.tempo_somatorio() - 2:
    # Adicionando as acelerações calculadas ponto a ponto da junta 1
    aceleracoes_angulares_theta1.append((velocidades_angulares_theta1[j + 1] - velocidades_angulares_theta1[j]) /
                                        trajetoria.infinitesimal())

    # Adicionando as acelerações calculadas ponto a ponto da junta 2
    aceleracoes_angulares_theta2.append((velocidades_angulares_theta2[j + 1] - velocidades_angulares_theta2[j]) /
                                        trajetoria.infinitesimal())

    j += 1

aceleracoes_angulares_theta1.append(0)  # Aceleração final é 0
aceleracoes_angulares_theta2.append(0)

# Calculando a energia gasta para movimentar a junta 1
torque_elo1_trajetoria_retilinea = calculo_torque_elo1(trajetoria.tempo_somatorio(), elo1.inercia(), elo1.massa(),
                                                       elo1.comprimento(), elo2.inercia(), elo2.massa(),
                                                       elo2.comprimento(), pontos_interm_espaco_junta1,
                                                       pontos_interm_espaco_junta2, aceleracoes_angulares_theta1,
                                                       aceleracoes_angulares_theta2, velocidades_angulares_theta1,
                                                       velocidades_angulares_theta2, motor.torque_atrito(),
                                                       motor.momento_inercia_motor(),
                                                       motor.coeficiente_atrito_viscoso())

energia_movimento_elo1_trajetoria_retilinea = energia_elo_i(trajetoria.tempo_somatorio(),
                                                            torque_elo1_trajetoria_retilinea,
                                                            motor.constante_torque_motor(),
                                                            motor.resistencia_armadura(),
                                                            motor.indutancia_armadura(),
                                                            motor.constante_proporcionalidade_tensao_velocidade(),
                                                            trajetoria.infinitesimal(),
                                                            velocidades_angulares_theta1)

# Calculando a energia gasta para movimentar a junta 2
torque_elo2_trajetoria_retilinea = calculo_torque_elo2(trajetoria.tempo_somatorio(), elo1.comprimento(),
                                                       elo2.inercia(), elo2.massa(), elo2.comprimento(),
                                                       pontos_interm_espaco_junta1, pontos_interm_espaco_junta2,
                                                       aceleracoes_angulares_theta1, aceleracoes_angulares_theta2,
                                                       velocidades_angulares_theta2, motor.torque_atrito(),
                                                       motor.momento_inercia_motor(),
                                                       motor.coeficiente_atrito_viscoso())

energia_movimento_elo2_trajetoria_retilinea = energia_elo_i(trajetoria.tempo_somatorio(),
                                                            torque_elo2_trajetoria_retilinea,
                                                            motor.constante_torque_motor(),
                                                            motor.resistencia_armadura(),
                                                            motor.indutancia_armadura(),
                                                            motor.constante_proporcionalidade_tensao_velocidade(),
                                                            trajetoria.infinitesimal(),
                                                            velocidades_angulares_theta2)

# Criação de gráficos para exibir os resultados do movimento composto.
print('Movimento com ambas as juntas se movendo ao traçar uma linha reta: \n')
print(f'Energia total requerida para mover a junta 1: {energia_movimento_elo1_trajetoria_retilinea}J '
      f'e a junta 2: {energia_movimento_elo2_trajetoria_retilinea}J, '
      f'totalizando {energia_movimento_elo1_trajetoria_retilinea + energia_movimento_elo2_trajetoria_retilinea}J')
print('\n')
eixo_y_grafico_PIJ1 = list(map(lambda pontos_y_pij1: conversao_radiano_grau(pontos_y_pij1),
                               pontos_interm_espaco_junta1))
criar_grafico(list(range(trajetoria.tempo_somatorio())), eixo_y_grafico_PIJ1,
              "Tempo (ms)", "Theta 1 (graus)", "Posições Intermediárias da Junta 1 - Plano Juntas",
              min(list(range(trajetoria.tempo_somatorio()))), max(list(range(trajetoria.tempo_somatorio()))), 1000,
              min(eixo_y_grafico_PIJ1), max(eixo_y_grafico_PIJ1), 5)

print('\n')
eixo_y_grafico_VAJ1 = list(map(lambda pontos_y_vaj1: conversao_radiano_grau(pontos_y_vaj1),
                               velocidades_angulares_theta1))
criar_grafico(list(range(trajetoria.tempo_somatorio())), eixo_y_grafico_VAJ1,
              "Tempo (ms)", "Velocidade Angular (graus/s)", "Velocidade Angular da Junta 1",
              min(list(range(trajetoria.tempo_somatorio()))), max(list(range(trajetoria.tempo_somatorio()))), 1000,
              min(eixo_y_grafico_VAJ1), max(eixo_y_grafico_VAJ1), 2)

print('\n')
eixo_y_grafico_AAJ1 = list(map(lambda pontos_y_aaj1: conversao_radiano_grau(pontos_y_aaj1),
                               aceleracoes_angulares_theta1))
criar_grafico(list(range(trajetoria.tempo_somatorio())), eixo_y_grafico_AAJ1,
              "Tempo (ms)", "Aceleração Angular (graus/s²)", "Aceleração Angular da Junta 1",
              min(list(range(trajetoria.tempo_somatorio()))), max(list(range(trajetoria.tempo_somatorio()))), 1000,
              min(eixo_y_grafico_AAJ1), max(eixo_y_grafico_AAJ1), 2)

print('\n')
eixo_y_grafico_PIJ2 = list(map(lambda pontos_y_pij2: conversao_radiano_grau(pontos_y_pij2),
                               pontos_interm_espaco_junta2))
criar_grafico(list(range(trajetoria.tempo_somatorio())), eixo_y_grafico_PIJ2,
              "Tempo (ms)", "Theta 2 (graus)", "Posições Intermediárias da Junta 2 - Plano Juntas",
              min(list(range(trajetoria.tempo_somatorio()))), max(list(range(trajetoria.tempo_somatorio()))), 1000,
              min(eixo_y_grafico_PIJ2), max(eixo_y_grafico_PIJ2), 5)

print('\n')
eixo_y_grafico_VAJ2 = list(map(lambda pontos_y_vaj2: conversao_radiano_grau(pontos_y_vaj2),
                               velocidades_angulares_theta2))
criar_grafico(list(range(trajetoria.tempo_somatorio())), eixo_y_grafico_VAJ2,
              "Tempo (ms)", "Velocidade Angular (graus/s)", "Velocidade Angular da Junta 2",
              min(list(range(trajetoria.tempo_somatorio()))), max(list(range(trajetoria.tempo_somatorio()))), 1000,
              min(eixo_y_grafico_VAJ2), max(eixo_y_grafico_VAJ2), 2)

print('\n')
eixo_y_grafico_AAJ2 = list(map(lambda pontos_y_aaj2: conversao_radiano_grau(pontos_y_aaj2),
                               aceleracoes_angulares_theta2))
criar_grafico(list(range(trajetoria.tempo_somatorio())), eixo_y_grafico_AAJ2,
              "Tempo (ms)", "Aceleração Angular (graus/s²)", "Aceleração Angular da Junta 2",
              min(list(range(trajetoria.tempo_somatorio()))), max(list(range(trajetoria.tempo_somatorio()))), 1000,
              min(eixo_y_grafico_AAJ2), max(eixo_y_grafico_AAJ2), 2)

pontos_interm_espaco_cartesiano_x_movi2 = list()
pontos_interm_espaco_cartesiano_y_movi2 = list()

for z in range(trajetoria.tempo_somatorio()):
    pontos_x, pontos_y = cinematica_direta_posicoes_x_y(pontos_interm_espaco_junta1[z],
                                                        pontos_interm_espaco_junta2[z],
                                                        elo1.comprimento(), elo2.comprimento())
    pontos_interm_espaco_cartesiano_x_movi2.append(pontos_x)
    pontos_interm_espaco_cartesiano_y_movi2.append(pontos_y)

print('\n')
criar_grafico(pontos_interm_espaco_cartesiano_x_movi2, pontos_interm_espaco_cartesiano_y_movi2,
              "Pontos no eixo X do espaço cartesiano", "Pontos no eixo Y do espaço cartesiano",
              "Posições intermediárias - Plano Cartesiano",
              min(pontos_interm_espaco_cartesiano_x_movi2), max(pontos_interm_espaco_cartesiano_x_movi2), 0.25,
              min(pontos_interm_espaco_cartesiano_y_movi2), max(pontos_interm_espaco_cartesiano_y_movi2), 0.25)
