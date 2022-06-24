import itertools
import matplotlib.pyplot as plt
from funcoes import Cidade, escreve_resultados_e_os_retorna, ler_cidades,visualizar_PCV, escreve_cidades_e_retorna_elas, gera_cidades_aleatorias, custo_caminho


def resolve_pcv_dinamicamente(cidades):
    distancia_matrix = [[x.distancia(y) for y in cidades] for x in cidades]
    cidades_a = {(frozenset([0, idx + 1]), idx + 1): (dist, [0, idx + 1]) for idx, dist in
                enumerate(distancia_matrix[0][1:])}
    for m in range(2, len(cidades)):
        cidades_b = {}
        for cidades_set in [frozenset(C) | {0} for C in itertools.combinations(range(1, len(cidades)), m)]:
            for j in cidades_set - {0}:
                cidades_b[(cidades_set, j)] = min([(cidades_a[(cidades_set - {j}, k)][0] + distancia_matrix[k][j],
                                                  cidades_a[(cidades_set - {j}, k)][1] + [j])
                                                 for k in cidades_set if k != 0 and k != j])
        cidades_a = cidades_b
    res = min([(cidades_a[d][0] + distancia_matrix[0][d[1]], cidades_a[d][1]) for d in iter(cidades_a)])
    print(cidades)
    return res[1]


num_cidades = 8
nome_metodo = "programacao_dinamica"

if __name__ == "__main__":

    cidades = ler_cidades(num_cidades)
    aux = resolve_pcv_dinamicamente(cidades)
    solucao = [cidades[auxi] for auxi in aux]
    print(custo_caminho(solucao))
    resultante = custo_caminho(solucao)
    escreve_resultados_e_os_retorna(nome_metodo, resultante, num_cidades, solucao)
    visualizar_PCV('Programação dinamica', solucao)
    plt.show(block=True)
