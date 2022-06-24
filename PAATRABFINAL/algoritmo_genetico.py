import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
import math, sys
import random
from funcoes import Cidade, ler_cidades,escreve_resultados_e_os_retorna, escreve_cidades_e_retorna_elas, gera_cidades_aleatorias


class Forca:
    def __init__(self, rota):
        self.rota = rota
        self.distancia = 0
        self.forca = 0.0

    def custo_caminho(self):
        if self.distancia == 0:
            distancia = 0
            for index, cidade in enumerate(self.rota):
                distancia += cidade.distancia(self.rota[(index + 1) % len(self.rota)])
            self.distancia = distancia
        return self.distancia

    def path_forca(self):
        if self.forca == 0:
            self.forca = 1 / float(self.custo_caminho())
        return self.forca


class algoritmoGenetico:
    def __init__(self, iteracoes, populacao_tamanho, cidades, elites_num, ritmo_de_mutacao,
                 semente_gulosa=0, selecao_aleatoria=True, plot_progresso=True):
        self.plot_progresso = plot_progresso
        self.selecao_aleatoria = selecao_aleatoria
        self.progress = []
        self.ritmo_de_mutacao = ritmo_de_mutacao
        self.cidades = cidades
        self.elites_num = elites_num
        self.iteracoes = iteracoes
        self.populacao_tamanho = populacao_tamanho
        self.semente_gulosa = semente_gulosa

        self.populacao = self.initial_populacao()
        self.average_custo_caminho = 1
        self.classificacao_populacional = None

    def melhor_cromossomo(self):
        return self.classificacao_populacional[0][0]

    def melhor_distancia(self):
        return 1 / self.classificacao_populacional[0][1]

    def random_rota(self):
        return random.sample(self.cidades, len(self.cidades))

    def initial_populacao(self):
        p1 = [self.random_rota() for _ in range(self.populacao_tamanho - self.semente_gulosa)]
        guloso_populacao = [rota_gulosa(start_index % len(self.cidades), self.cidades)
                             for start_index in range(self.semente_gulosa)]
        return [*p1, *guloso_populacao]

    def rank_populacao(self):
        forca = [(chromosome, Forca(chromosome).path_forca()) for chromosome in self.populacao]
        self.classificacao_populacional = sorted(forca, key=lambda f: f[1], reverse=True)

    def selecao(self):
        selecoes = [self.classificacao_populacional[i][0] for i in range(self.elites_num)]
        if self.selecao_aleatoria:
            df = pd.DataFrame(np.array(self.classificacao_populacional), columns=["index", "forca"])
            self.average_custo_caminho = sum(1 / df.forca) / len(df.forca)
            df['cum_sum'] = df.forca.cumsum()
            df['cum_perc'] = 100 * df.cum_sum / df.forca.sum()

            for _ in range(0, self.populacao_tamanho - self.elites_num):
                pick = 100 * random.random()
                for i in range(0, len(self.classificacao_populacional)):
                    if pick <= df.iat[i, 3]:
                        selecoes.append(self.classificacao_populacional[i][0])
                        break
        else:
            for _ in range(0, self.populacao_tamanho - self.elites_num):
                pick = random.randint(0, self.populacao_tamanho - 1)
                selecoes.append(self.classificacao_populacional[pick][0])
        self.populacao = selecoes

    @staticmethod
    def produzir_crianca(parent1, parent2):
        gene_1 = random.randint(0, len(parent1))
        gene_2 = random.randint(0, len(parent1))
        gene_1, gene_2 = min(gene_1, gene_2), max(gene_1, gene_2)
        crianca = [parent1[i] for i in range(gene_1, gene_2)]
        crianca.extend([gene for gene in parent2 if gene not in crianca])
        return crianca

    def gerar_populacao(self):
        length = len(self.populacao) - self.elites_num
        crianca = self.populacao[:self.elites_num]
        for i in range(0, length):
            child = self.produzir_crianca(self.populacao[i],
                                       self.populacao[(i + random.randint(1, self.elites_num)) % length])
            crianca.append(child)
        return crianca

    def mutar(self, individuo):
        for index, cidade in enumerate(individuo):
            if random.random() < max(0, self.ritmo_de_mutacao):
                tamanho_amostra = min(min(max(3, self.populacao_tamanho // 5), 100), len(individuo))
                amostra_aleatoria = random.sample(range(len(individuo)), tamanho_amostra)
                amostra_ordenada = sorted(amostra_aleatoria,
                                       key=lambda c_i: individuo[c_i].distancia(individuo[index - 1]))
                index_aleatorio_final = random.choice(amostra_ordenada[:max(tamanho_amostra // 3, 2)])
                individuo[index], individuo[index_aleatorio_final] = \
                    individuo[index_aleatorio_final], individuo[index]
        return individuo

    def proxima_geracao(self):
        self.rank_populacao()
        self.selecao()
        self.populacao = self.gerar_populacao()
        self.populacao[self.elites_num:] = [self.mutar(chromosome)
                                             for chromosome in self.populacao[self.elites_num:]]

    def run(self):
        if self.plot_progresso:
            plt.ion()
        for ind in range(0, self.iteracoes):
            self.proxima_geracao()
            self.progress.append(self.melhor_distancia())
            if self.plot_progresso and ind % 10 == 0:
                self.plot()
            elif not self.plot_progresso and ind % 10 == 0:
                print(self.melhor_distancia())

    def plot(self):
        print(self.melhor_distancia())
        fig = plt.figure(0)
        plt.plot(self.progress, 'g')
        fig.suptitle('gerações do algoritmo genético')
        plt.ylabel('distancia')
        plt.xlabel('Geração')

        x_list, y_list = [], []
        for cidade in self.melhor_cromossomo():
            x_list.append(cidade.x)
            y_list.append(cidade.y)
        x_list.append(self.melhor_cromossomo()[0].x)
        y_list.append(self.melhor_cromossomo()[0].y)
        fig = plt.figure(1)
        fig.clear()
        fig.suptitle('PCV Algoritmo genetico')
        plt.plot(x_list, y_list, 'ro')
        plt.plot(x_list, y_list, 'g')

        if self.plot_progresso:
            plt.draw()
            plt.pause(0.05)
        plt.show()


def rota_gulosa(start_index, cidades):
    nao_visitado = cidades[:]
    del nao_visitado[start_index]
    rota = [cidades[start_index]]
    while len(nao_visitado):
        index, nearest_cidade = min(enumerate(nao_visitado), key=lambda item: item[1].distancia(rota[-1]))
        rota.append(nearest_cidade)
        del nao_visitado[index]
    return rota

num_cidades = 8
nome_metodo = "algoritmo_genetico"
num_iteracoes = 100 
tam_populacao = 100
num_elites = 20
prob_mutacao = 0.008
semente_gulosa = 1

if __name__ == '__main__':
    cidades = ler_cidades(num_cidades)
    genetic_algorithm = algoritmoGenetico(cidades=cidades, iteracoes=num_iteracoes, populacao_tamanho=tam_populacao,
                                         elites_num=num_elites, ritmo_de_mutacao=prob_mutacao, semente_gulosa=semente_gulosa,
                                         selecao_aleatoria=True, plot_progresso=True)
    genetic_algorithm.run()
    resultante = genetic_algorithm.melhor_distancia()
    #print(resultante)
    genetic_algorithm.plot()
    escreve_resultados_e_os_retorna(nome_metodo, resultante, num_cidades, genetic_algorithm.cidades)
    plt.show(block=True)
