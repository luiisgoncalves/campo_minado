import numpy as np
from random import randint


class Campo:
    def __init__(self, linhas, colunas, elemento='·'):
        self.linhas = linhas
        self.colunas = colunas
        self.elemento = elemento
        self.campo = np.full((linhas, colunas), elemento)

    def mostra_campo(self, campo_minado=None, espacamento='   '):
        # print da numeracao das colunas
        for i in range(self.colunas):
            print(i, end=espacamento)

        print('\n' + '-- ' * (((self.colunas + self.colunas * len(espacamento)) // 3) + 1))

        # mostrar o campo minado
        for j in range(self.linhas):
            for k in range(self.colunas):
                if campo_minado is None:
                    print(self.campo[j][k], end=espacamento)
                else:
                    print(campo_minado[j][k], end=espacamento)

            # print da numeracao das linhas
            print('¦', j)


class CampoMinado(Campo):
    def __init__(self, linhas, colunas, dificulade, elemento='·', bomba='X'):
        super().__init__(linhas, colunas, elemento)
        self.dificuldade = dificulade
        self.bomba = bomba
        self.maximo = self.linhas * self.colunas
        self.campo_minado = np.copy(self.campo)

    def cria_bombas(self):
        maximo = self.linhas * self.colunas
        bombas = []
        quantidade_bombas = int(self.dificuldade * maximo)
        i = 0
        while i < quantidade_bombas:
            posicao_bomba = randint(0, maximo - 1)
            if posicao_bomba not in bombas:
                bombas.append(posicao_bomba)
                i += 1

        ######################
        # print(len(bombas))
        # bombas.sort()
        # print(bombas)
        ######################

        self.adiciona_bombas(bombas)

    def adiciona_bombas(self, bombas):
        for bomba in bombas:
            linha = bomba // self.colunas
            coluna = bomba % self.colunas
            self.campo_minado[linha][coluna] = self.bomba

    def conta_bombas(self):
        dimensao = [-1, 0, 1]

        for linha in range(self.linhas):
            for coluna in range(self.colunas):

                matriz_index = np.array([], dtype=int)

                ###########################################################################################################
                # line_inf = linha - 1 if linha - 1 >= 0 else 0
                # line_sup = linha + 1
                # column_inf = coluna - 1 if coluna - 1 >= 0 else 0
                # column_sup = coluna + 1
                # matriz_index = np.append(matriz_index, self.campo_minado[line_inf:line_sup+1, column_inf:column_sup+1])
                # print(matriz_index)
                ###########################################################################################################

                for i in range(3):
                    for j in range(3):
                        line = linha + dimensao[i]
                        column = coluna + dimensao[j]

                        matriz_index = np.append(matriz_index, [line, column])

                matriz_index = matriz_index.reshape((9, 2))

                if self.campo_minado[linha][coluna] != self.bomba:
                    qntd_bomba = 0
                    for item in matriz_index:
                        line, column = item
                        if 0 <= column < self.linhas and 0 <= line < self.colunas:
                            qntd_bomba = qntd_bomba + 1 if self.campo_minado[line][column] == self.bomba else qntd_bomba
                    self.campo_minado[linha][coluna] = qntd_bomba
