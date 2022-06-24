import matplotlib.pyplot as plt
from funcoes import Cidade, ler_cidades, escreve_resultados_e_os_retorna, escreve_cidades_e_retorna_elas, gera_cidades_aleatorias, custo_caminho


class Guloso:
    def __init__(self, cidades):
        self.nao_visitado = cidades[1:]
        self.rota = [cidades[0]]

    def run(self, plot):
        if plot:
            plt.ion()
            plt.show(block=False)
            self.init_plot()
        while len(self.nao_visitado):
            index, cidade_mProxima = min(enumerate(self.nao_visitado),
                                      key=lambda item: item[1].distancia(self.rota[-1]))
            self.rota.append(cidade_mProxima)
            del self.nao_visitado[index]
            self.plot_interactive(False)
        self.rota.append(self.rota[0])
        self.plot_interactive(False)
        self.rota.pop()
        return custo_caminho(self.rota)

    def plot_interactive(self, block):
        x1, y1, x2, y2 = self.rota[-2].x, self.rota[-2].y, self.rota[-1].x, self.rota[-1].y
        plt.plot([x1, x2], [y1, y2], 'ro')
        plt.plot([x1, x2], [y1, y2], 'g')
        plt.draw()
        plt.pause(0.07)
        plt.show(block=block)

    def init_plot(self):
        fig = plt.figure(0)
        fig.suptitle('PCV abordagem Gulosa')
        x_list, y_list = [], []
        for cidade in [*self.rota, *self.nao_visitado]:
            x_list.append(cidade.x)
            y_list.append(cidade.y)
        x_list.append(self.rota[0].x)
        y_list.append(self.rota[0].y)

        plt.plot(x_list, y_list, 'ro')
        plt.show(block=False)

num_cidades = 8
nome_metodo = "algoritmo_guloso"


if __name__ == "__main__":
    cidades = ler_cidades(num_cidades)
    guloso = Guloso(cidades)
    resultante = guloso.run(plot=True)
    escreve_resultados_e_os_retorna(nome_metodo, resultante, num_cidades, guloso.rota)
    print(resultante)
    print(guloso.rota)
    plt.show(block=True)
