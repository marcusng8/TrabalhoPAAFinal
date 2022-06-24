import math
import random
import matplotlib.pyplot as plt

class Cidade:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distancia(self, cidade):
        return math.hypot(self.x - cidade.x, self.y - cidade.y)

    def __repr__(self):
        return f"({self.x}, {self.y})"


def ler_cidades(tamanho):
    cidades = []
    with open(f'entrada_teste/cidades_{tamanho}.data', 'r') as handle:
        lines = handle.readlines()
        for line in lines:
            x, y = map(float, line.split())
            cidades.append(Cidade(x, y))
    return cidades

def gera_cidades_aleatorias(tamanho):
    return [Cidade(x=int(random.random() * 1000), y=int(random.random() * 1000)) for _ in range(tamanho)]


def custo_caminho(rota):
    return sum([cidade.distancia(rota[index - 1]) for index, cidade in enumerate(rota)])


def visualizar_PCV(titulo, cidades):
    fig = plt.figure()
    fig.suptitle(titulo)
    x_list, y_list = [], []
    for cidade in cidades:
        x_list.append(cidade.x)
        y_list.append(cidade.y)
    x_list.append(cidades[0].x)
    y_list.append(cidades[0].y)

    plt.plot(x_list, y_list, 'ro')
    plt.plot(x_list, y_list, 'g')
    plt.show(block=True)

def escreve_cidades_e_retorna_elas(tamanho):
    cidades = gera_cidades_aleatorias(tamanho)
    with open(f'entrada_teste/cidades_{tamanho}.data', 'w+') as handle:
        for cidade in cidades:
            handle.write(f'{cidade.x} {cidade.y}\n')
    return cidades

def escreve_resultados_e_os_retorna(nome_metodo, resultante, num_cidades, cidades):
    with open(f'saida_resultado/cidades_resultado_{num_cidades}_{nome_metodo}.data', 'w+') as handle:
        handle.write(str(resultante)+ '\n')
        for cidade in cidades:
            handle.write(f'{cidade.x} {cidade.y}\n')
    return cidades
