from matplotlib.pyplot import show, subplots, xticks, yticks
from numpy import arange


def criar_grafico(dados_eixo_x, dados_eixo_y,
                  nome_eixo_x, nome_eixo_y, titulo_grafico,
                  valor_min_eixo_x, valor_max_eixo_x, tamanho_espacamento_eixo_x,
                  valor_min_eixo_y, valor_max_eixo_y, tamanho_espacamento_eixo_y):
    """
    A função "criar_grafico" visa plotar uma curva com os dados fornecidos.
    Variáveis:
    dados_eixo_x = Coordenada X das posições no plano cartesiano;
    dados_eixo_y = Coordenada Y das posições no plano cartesiano;
    nome_eixo_x = Nome desejado para o eixo X;
    nome_eixo_y = Nome desejado para o eixo Y;
    titulo_grafico = Título desejado para o gráfico;
    """
    eixo_x = dados_eixo_x  # Criando os valores da função no eixo x
    eixo_y = dados_eixo_y  # Adicionando os valores da função no eixo y
    fig, grafico = subplots()  # Criando um gráfico
    grafico.plot(eixo_x, eixo_y, label='')  # Adicionando os valores da função no gráfico
    grafico.set_xlabel(nome_eixo_x)  # Adicionando o nome do eixo x
    grafico.set_ylabel(nome_eixo_y)  # Adicionando o nome do eixo y
    grafico.set_title(titulo_grafico)  # Adicionando o título do gráfico
    xticks(arange(valor_min_eixo_x - tamanho_espacamento_eixo_x,
                  valor_max_eixo_x + tamanho_espacamento_eixo_x,
                  tamanho_espacamento_eixo_x))  # Modificando a grade do eixo x
    yticks(arange(valor_min_eixo_y - tamanho_espacamento_eixo_y,
                  valor_max_eixo_y + tamanho_espacamento_eixo_y,
                  tamanho_espacamento_eixo_y))  # Modificando a grade do eixo y
    grafico.grid()
    show()
