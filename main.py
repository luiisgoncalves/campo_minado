# from random import randint


def controi_campo(tamanho, espacamento='   ', elemento='·'):
    linhas = tamanho[0]
    colunas = tamanho[1]
    campo_minado = []

    # construir o campo minado vazio
    for i in range(linhas):
        linha = []
        for j in range(colunas):
            linha.append(elemento)
        campo_minado.append(linha)

    # print da numeracao das colunas
    for i in range(colunas):
        print(i, end=espacamento)
    print()

    # mostrar o campo minado
    for j in range(linhas):
        for k in range(colunas):
            print(campo_minado[j][k], end=espacamento)

        # print da numeracao das linhas
        print(j)

    return campo_minado


controi_campo([5, 5])
