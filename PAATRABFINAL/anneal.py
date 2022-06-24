import math
import random
import matplotlib.pyplot as plt
from funcoes import Cidade, ler_cidades,escreve_resultados_e_os_retorna, escreve_cidades_e_retorna_elas, gera_cidades_aleatorias, visualizar_PCV, custo_caminho

class SimAnneal(object):
    def __init__(self, cidades, temperatura=-1, alpha=-1, temperatura_de_parada=-1, iterac_de_parada=-1):
        self.cidades = cidades
        self.num_cidades = len(cidades)
        self.temperatura = math.sqrt(self.num_cidades) if temperatura == -1 else temperatura
        self.T_save = self.temperatura
        self.alpha = 0.999 if alpha == -1 else alpha
        self.temperatura_de_parada = 1e-8 if temperatura_de_parada == -1 else temperatura_de_parada
        self.iterac_de_parada = 100000 if iterac_de_parada == -1 else iterac_de_parada
        self.iteracao = 1
        self.rota = None
        self.melhor_forca = float("Inf")
        self.progresso = []
        self.cur_cost = None

    def solucao_gulosa(self):
        incia_vertice = random.randint(0, self.num_cidades)  # Inicia em um vertice aleatorio
        nao_visitado = self.cidades[:]
        del nao_visitado[incia_vertice]
        rota = [cidades[incia_vertice]]
        while len(nao_visitado):
            index, cidade_mProxima = min(enumerate(nao_visitado), key=lambda item: item[1].distancia(rota[-1]))
            rota.append(cidade_mProxima)
            del nao_visitado[index]
        custo_atual = custo_caminho(rota)
        self.progresso.append(custo_atual)
        return rota, custo_atual

    def probabilidade_de_aceitar(self, forca_do_candidato):
        return math.exp(-abs(forca_do_candidato - self.cur_cost) / self.temperatura)

    def accept(self, chute):
        chuta_custo = custo_caminho(chute)
        if chuta_custo < self.cur_cost:
            self.cur_cost, self.rota = chuta_custo, chute
            if chuta_custo < self.melhor_forca:
                self.melhor_forca, self.rota = chuta_custo, chute
        else:
            if random.random() < self.probabilidade_de_aceitar(chuta_custo):
                self.cur_cost, self.rota = chuta_custo, chute

    def run(self):
        self.rota, self.cur_cost = self.solucao_gulosa()
        while self.temperatura >= self.temperatura_de_parada and self.iteracao < self.iterac_de_parada:
            chute = list(self.rota)
            index_esquerdo = random.randint(2, self.num_cidades - 1)
            index_direito = random.randint(0, self.num_cidades - index_esquerdo)
            chute[index_direito: (index_direito + index_esquerdo)] = reversed(chute[index_direito: (index_direito + index_esquerdo)])
            self.accept(chute)
            self.temperatura *= self.alpha
            self.iteracao += 1
            self.progresso.append(self.cur_cost)

        print("Melhor força obtida: ", self.melhor_forca)

    def visualize_rotas(self):
        visualizar_PCV('Anneal PCV', self.rota)

    def plot_learning(self):
        fig = plt.figure(1)
        plt.plot([i for i in range(len(self.progresso))], self.progresso)
        plt.ylabel("distancia")
        plt.xlabel("iteração")
        plt.show(block=False)

num_cidades = 4
nome_metodo = "algoritmo_anneal"

if __name__ == "__main__":
    cidades = ler_cidades(num_cidades)
    solucao = SimAnneal(cidades, iterac_de_parada=15000)
    solucao.run()
    solucao.plot_learning()
    resultante = solucao.melhor_forca
    escreve_resultados_e_os_retorna(nome_metodo, resultante, num_cidades, solucao.cidades)
    solucao.visualize_rotas()
