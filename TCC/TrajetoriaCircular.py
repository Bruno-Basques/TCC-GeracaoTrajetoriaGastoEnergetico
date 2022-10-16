from Model.EloModel import Elo
from Model.MotorModel import Motor
from Model.MovimentoModel import Movimento
from Services.AceleracaoService import aceleracao_angular
from Services.CinematicaService import cinematica_direta_posicoes_x_y
from Services.EnergiaService import energia_elo_i
from Services.GraficoService import criar_grafico
from Services.TorqueService import calculo_torque_elo1
from Services.TrajetoriaService import tempo_transicao_parabolico_linear, trajetoria_linear_simples
from Services.VelocidadeService import velocidade_angular
from TCC.Services.ConversaoUnidadesService import conversao_grau_radiano, conversao_radiano_grau

# Criação dos objetos motor, elos (1 e 2) e movimento.

motor = Motor(1, 0.046, 0.093, 0, 0.008, 0.55, 0.55)
elo1 = Elo(2700, 0.05, 0.5)
elo2 = Elo(2700, 0.05, 0.5)
trajetoria = Movimento(conversao_grau_radiano(15), conversao_grau_radiano(105),
                       conversao_grau_radiano(60), conversao_grau_radiano(60), 10, 0.001)

# Início do cálculo da energia gasta para movimentar o planar de dois graus de liberdade com a junta 2 fixa.

# Calculo da aceleração do movimento da junta 1 com a junta 2 fixa.
aceleracao_constante = aceleracao_angular(trajetoria.theta1_inicial(), trajetoria.theta1_final(),
                                          trajetoria.tempo_somatorio())

aceleracao_constante = aceleracao_constante * 2

# Calculando o tempo que ocorre a primeira transição entre a parte parabólica e a linear da trajetória.
temp_parab_linea1 = tempo_transicao_parabolico_linear(trajetoria.tempo_somatorio(), aceleracao_constante,
                                                      trajetoria.theta1_final(), trajetoria.theta1_inicial())

# Calculando os valores que junta 1 assume durante a realização do movimento.
movimento_braco1 = trajetoria_linear_simples(trajetoria.tempo_somatorio(), trajetoria.theta1_inicial(),
                                             trajetoria.theta1_final(), aceleracao_constante)

# Criando uma lista com os valores da junta 2, que são sempre iguais ao valor inicial.
movimento_braco2 = list()
for f in range(trajetoria.tempo_somatorio()):
    movimento_braco2.append(trajetoria.theta2_inicial())

lista_velocidade_theta1 = list()
lista_aceleracao_theta1 = list()

lista_velocidade_theta2 = list()
lista_aceleracao_theta2 = list()

lista_velocidade_theta1.append(0)  # Adicionando a primeira velocidade como zero na lista de velocidades
lista_aceleracao_theta1.append(aceleracao_constante)  # Adicionando a primeira aceleração na lista de acelerações

lista_velocidade_theta2.append(0)
lista_aceleracao_theta2.append(0)

g = 0
while g < trajetoria.tempo_somatorio() - 1:
    # Calculando a velocidade angular e adicionando-a a uma lista de velocidades.
    lista_velocidade_theta1.append(velocidade_angular(movimento_braco1[g], movimento_braco1[g + 1],
                                                      trajetoria.infinitesimal()))

    # Adicionando a aceleração constante, não nula e positiva em uma lista de acelerações (parte parabólica).
    if g < temp_parab_linea1:
        lista_aceleracao_theta1.append(aceleracao_constante)

    # Adicionando a aceleração constante e nula em uma lista de acelerações (parte linear).
    elif temp_parab_linea1 <= g < (trajetoria.tempo_somatorio() - temp_parab_linea1):
        lista_aceleracao_theta1.append(0)

    # Adicionando a aceleração constante, não nula e negativa em uma lista de acelerações (parte parabólica).
    else:
        lista_aceleracao_theta1.append(-aceleracao_constante)

    lista_velocidade_theta2.append(0)
    lista_aceleracao_theta2.append(0)
    g += 1

# Calculando a energia gasta para movimentar o elo 1 na trajetória circular (com a junta 2 fixa).
torque_elo1_trajetoria_circular = calculo_torque_elo1(trajetoria.tempo_somatorio(), elo1.inercia(), elo1.massa(),
                                                      elo1.comprimento(), elo2.inercia(), elo2.massa(),
                                                      elo2.comprimento(), movimento_braco1, movimento_braco2,
                                                      lista_aceleracao_theta1, lista_aceleracao_theta2,
                                                      lista_velocidade_theta1, lista_velocidade_theta2,
                                                      motor.torque_atrito(), motor.momento_inercia_motor(),
                                                      motor.constante_proporcionalidade_tensao_velocidade())

energia_movimento_elo1_trajetoria_circular = energia_elo_i(trajetoria.tempo_somatorio(),
                                                           torque_elo1_trajetoria_circular,
                                                           motor.constante_torque_motor(),
                                                           motor.resistencia_armadura(),
                                                           motor.indutancia_armadura(),
                                                           motor.constante_proporcionalidade_tensao_velocidade(),
                                                           trajetoria.infinitesimal(),
                                                           lista_velocidade_theta1)

# Criação de gráficos para exibir os resultados do movimento simples.
print('Movimento com apenas a junta 1 se movendo ao traçar um arco: \n')
print('\n')
criar_grafico(list(range(trajetoria.tempo_somatorio())), movimento_braco1,
              "Tempo (ms)", "Theta (graus)", "Posições da Junta 1 - Cenário 1",
              min(list(range(trajetoria.tempo_somatorio()))), max(list(range(trajetoria.tempo_somatorio()))), 1000,
              min(movimento_braco1), max(movimento_braco1), max(movimento_braco1) / 10)
print('\n')
eixo_y_VAJ1 = list(map(lambda velocidade_theta1: conversao_radiano_grau(velocidade_theta1), lista_velocidade_theta1))
criar_grafico(list(range(trajetoria.tempo_somatorio())), eixo_y_VAJ1,
              "Tempo (ms)", "Velocidade (graus/s)", "Velocidades da Junta 1 - Cenário 1",
              min(list(range(trajetoria.tempo_somatorio()))), max(list(range(trajetoria.tempo_somatorio()))), 1000,
              min(eixo_y_VAJ1), max(eixo_y_VAJ1), max(eixo_y_VAJ1) / 10)

print('\n')
eixo_y_AAJ1 = list(map(lambda aceleracao_theta1: conversao_radiano_grau(aceleracao_theta1), lista_aceleracao_theta1))
criar_grafico(list(range(trajetoria.tempo_somatorio())), eixo_y_AAJ1,
              "Tempo (ms)", "Aceleração (graus/s²)", "Acelerações da Junta 1 - Cenário 1",
              min(list(range(trajetoria.tempo_somatorio()))), max(list(range(trajetoria.tempo_somatorio()))), 1000,
              min(eixo_y_AAJ1), max(eixo_y_AAJ1), max(eixo_y_AAJ1) / 10)
print('\n')
eixo_y_AAJ1 = torque_elo1_trajetoria_circular
criar_grafico(list(range(trajetoria.tempo_somatorio())), eixo_y_AAJ1,
              "Tempo (ms)", "Torque (N*m)", "Torques da Junta 1 - Cenário 1",
              min(list(range(trajetoria.tempo_somatorio()))), max(list(range(trajetoria.tempo_somatorio()))), 1000,
              min(eixo_y_AAJ1), max(eixo_y_AAJ1), max(eixo_y_AAJ1) / 10)

pontos_interm_espaco_cartesiano_x_movi1 = list()
pontos_interm_espaco_cartesiano_y_movi1 = list()

for z in range(trajetoria.tempo_somatorio()):
    pontos_x, pontos_y = cinematica_direta_posicoes_x_y(movimento_braco1[z],
                                                        movimento_braco2[z],
                                                        elo1.comprimento(), elo2.comprimento())
    pontos_interm_espaco_cartesiano_x_movi1.append(pontos_x)
    pontos_interm_espaco_cartesiano_y_movi1.append(pontos_y)

print('\n')
criar_grafico(pontos_interm_espaco_cartesiano_x_movi1, pontos_interm_espaco_cartesiano_y_movi1,
              "Pontos no eixo X do espaço cartesiano", "Pontos no eixo Y do espaço cartesiano",
              "Posições intermediárias - Plano Cartesiano",
              min(pontos_interm_espaco_cartesiano_x_movi1), max(pontos_interm_espaco_cartesiano_x_movi1), 0.25,
              min(pontos_interm_espaco_cartesiano_y_movi1), max(pontos_interm_espaco_cartesiano_y_movi1), 0.25)
print(f'Inercia do elo 1 e 2 {elo1.inercia()} kgm², {elo2.inercia()} kgm², respectivamente \n')
print('Energia requerida para executar o movimento completo:')
print(energia_movimento_elo1_trajetoria_circular, 'J\n')
