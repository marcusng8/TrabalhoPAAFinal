import matplotlib.pyplot as plt
import math
from funcoes import Cidade, escreve_resultados_e_os_retorna, ler_cidades, escreve_cidades_e_retorna_elas, gera_cidades_aleatorias

class Dividir_e_conquistar:
    def __init__(self, cidades):
        self.cidades = cidades
        self.rota = []

    def run(self):
        plt.ion()
        plt.show()
        self.rota = self.solve(self.cidades)
        print([aresta[0].distancia(aresta[1]) for aresta in self.rota])
        return sum([aresta[0].distancia(aresta[1]) for aresta in self.rota])

    def solve(self, cidades):
        if len(cidades) < 1:
            raise Exception('Recursão em cidades com tamanho < 0')
        elif len(cidades) == 1:
            return cidades[0]
        elif len(cidades) == 2:
            return [(cidades[0], cidades[1])]
        else:
            metade_1, metade_2 = self.dividir_mais_escuro(cidades)
            grafico_1 = self.solve(metade_1)
            grafico_2 = self.solve(metade_2)
            fusao = self.fusao(grafico_1, grafico_2)

            x = []
            y = []
            fig = plt.figure(0)
            fig.suptitle('PCV Dividir e conquistar')
            for cidade1, cidade2 in fusao:
                x.append(cidade1.x)
                x.append(cidade2.x)
                y.append(cidade1.y)
                y.append(cidade2.y)
                plt.plot([cidade1.x, cidade2.x], [cidade1.y, cidade2.y], 'c')

            plt.plot(x, y, 'ro')
            plt.draw()
            plt.pause(0.1)
            return fusao

    @staticmethod
    def dividir_mais_escuro(cidades):
        cidades_por_x = sorted(cidades, key=lambda cidade: cidade.x)
        cidades_por_y = sorted(cidades, key=lambda cidade: cidade.y)
        tamanho_medio = len(cidades_por_x) // 2
        if abs(cidades_por_x[0].x - cidades_por_x[-1].x) > abs(cidades_por_y[0].y - cidades_por_y[-1].y):
            return cidades_por_x[:tamanho_medio], cidades_por_x[tamanho_medio:]
        else:
            return cidades_por_y[:tamanho_medio], cidades_por_y[tamanho_medio:]

    def fusao(self, grafico_1, grafico_2):
        if isinstance(grafico_1, Cidade):
            grafico_2.append((grafico_1, grafico_2[0][0]))
            grafico_2.append((grafico_1, grafico_2[0][1]))
            return grafico_2
        custo_minimo = math.inf
        for aresta_index_1, (cidade_00, cidade_01) in enumerate(grafico_1):
            for aresta_index_2, (cidade_10, cidade_11) in enumerate(grafico_2):
                cost = cidade_00.distancia(cidade_10) + cidade_01.distancia(cidade_11) - \
                       cidade_00.distancia(cidade_01) - cidade_01.distancia(cidade_10)
                cost2 = cidade_00.distancia(cidade_11) + cidade_01.distancia(cidade_10) - \
                        cidade_00.distancia(cidade_01) - cidade_01.distancia(cidade_10)
                if cost < custo_minimo:
                    custo_minimo = cost
                    min_aresta_1 = (cidade_00, cidade_10)
                    min_aresta_2 = (cidade_01, cidade_11)
                    velha_aresta_index_1 = aresta_index_1
                    velha_aresta_index_2 = aresta_index_2
                if cost2 < custo_minimo:
                    custo_minimo = cost2
                    min_aresta_1 = (cidade_00, cidade_11)
                    min_aresta_2 = (cidade_01, cidade_10)
                    velha_aresta_index_1 = aresta_index_1
                    velha_aresta_index_2 = aresta_index_2
        if len(grafico_1) + len(grafico_2) > 4:
            del grafico_1[velha_aresta_index_1]
            del grafico_2[velha_aresta_index_2]
        elif len(grafico_1) + len(grafico_2) == 4:
            del grafico_2[velha_aresta_index_2]
        grafico_1.extend([min_aresta_1, min_aresta_2])
        grafico_1.extend(grafico_2)
        return grafico_1
x = []
y = []
num_cidades = 4
nome_metodo = "dividir_e_conquistar"

if __name__ == "__main__":
    for _ in range(1):
        cidades = ler_cidades(num_cidades)
        dividir_e_conquistar = Dividir_e_conquistar(cidades)
        resultante = dividir_e_conquistar.run()
        print(resultante)
        print(dividir_e_conquistar.rota)
        escreve_resultados_e_os_retorna(nome_metodo, resultante, num_cidades, dividir_e_conquistar.cidades)
        fig = plt.figure(0)
        fig.suptitle('PCV - Dividir e Conquistar')
        for cidade1, cidade2 in dividir_e_conquistar.rota:
            x.append(cidade1.x)
            x.append(cidade2.x)
            y.append(cidade1.y)
            y.append(cidade2.y)
            plt.plot([cidade1.x, cidade2.x], [cidade1.y, cidade2.y], 'g')

        plt.plot(x, y, 'ro')
        plt.show(block=True)
