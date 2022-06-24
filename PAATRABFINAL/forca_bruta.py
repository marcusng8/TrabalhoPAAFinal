import itertools
from funcoes import Cidade, escreve_resultados_e_os_retorna, ler_cidades, escreve_cidades_e_retorna_elas, gera_cidades_aleatorias, custo_caminho, visualizar_PCV

class forcaBruta:
    def __init__(self, cidades):
        self.cidades = cidades

    def run(self):
        self.cidades = min(itertools.permutations(self.cidades), key=lambda path: custo_caminho(path))
        return custo_caminho(self.cidades)

num_cidades = 4
nome_metodo = "forca_bruta"

if __name__ == "__main__":

    brute = forcaBruta(ler_cidades(num_cidades))
    resultante = brute.run()
    print(resultante)
    #print(brute.run())
    escreve_resultados_e_os_retorna(nome_metodo, resultante, num_cidades, brute.cidades)
    visualizar_PCV('Força Bruta PCV', brute.cidades)
