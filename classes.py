import numpy as np
from random import randint, seed

seed(47)


class Campo:
    def __init__(self, linhas, colunas, elemento='·'):
        self.linhas = linhas
        self.colunas = colunas
        self.elemento = elemento
        self.campo = np.full((linhas, colunas), elemento)

    def mostra_campo(self, campo_minado=None, espacamento='   '):
        # print da numeracao das colunas
        for i in range(self.colunas):
            print(str(i).ljust(len(espacamento) + 1), end='')

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
        for linha in range(self.linhas):
            for coluna in range(self.colunas):

                matriz_index = self.redondezas(linha, coluna)

                if self.campo_minado[linha][coluna] != self.bomba:
                    qntd_bomba = 0
                    for item in matriz_index:
                        line, column = item
                        if 0 <= column < self.linhas and 0 <= line < self.colunas:
                            qntd_bomba = qntd_bomba + 1 if self.campo_minado[line][column] == self.bomba else qntd_bomba
                    self.campo_minado[linha][coluna] = qntd_bomba

    def ver_elementos(self, linha, coluna):
        matriz = self.redondezas(linha, coluna)
        sub_matriz = np.array([], dtype=int)

        for elemento in matriz:
            if 0 <= elemento[0] < self.linhas and 0 <= elemento[1] < self.colunas:
                item = int(self.campo_minado[elemento[0], elemento[1]]) if self.campo_minado[elemento[0], elemento[1]] != self.bomba else -1
                sub_matriz = np.append(sub_matriz, item)

        match len(sub_matriz):
            case 4:
                sub_matriz = sub_matriz.reshape((2, 2))
            case 6:
                if matriz[0, 1] == -1 or matriz[9, 1] == self.colunas:
                    sub_matriz = sub_matriz.reshape((3, 2))
                else:
                    sub_matriz = sub_matriz.reshape((2, 3))
            case 9:
                sub_matriz = sub_matriz.reshape((3, 3))

        # print(sub_matriz)
        return sub_matriz

    def redondezas(self, linha, coluna):
        dimensao = [-1, 0, 1]
        matriz_index = np.array([], dtype=int)

        ###########################################################################################################
        # line_inf = linha - 1 if linha - 1 >= 0 else 0
        # line_sup = linha + 2
        # column_inf = coluna - 1 if coluna - 1 >= 0 else 0
        # column_sup = coluna + 2
        # matriz_index = np.append(matriz_index, self.campo_minado[line_inf:line_sup, column_inf:column_sup])
        # print(matriz_index)
        ###########################################################################################################

        for i in range(3):
            for j in range(3):
                line = linha + dimensao[i]
                column = coluna + dimensao[j]

                if 0 <= line < self.linhas and 0 <= column < self.colunas:
                    matriz_index = np.append(matriz_index, [line, column])
        # print(matriz_index.reshape((9, 2)))
        # print('\n')
        return matriz_index.reshape((-1, 2))

    def escolha(self, linha, coluna):
        if self.campo_minado[linha, coluna] == self.bomba:
            self.explosao()
            return True
        elif int(self.campo_minado[linha, coluna]) == 0:
            livres = self.sem_bomba(linha, coluna)
            for livre in livres:
                line, column = livre
                self.campo[line, column] = self.campo_minado[line, column]
            return False
        else:
            self.campo[linha, coluna] = self.campo_minado[linha, coluna]
            return False

    def explosao(self):
        for i in range(self.linhas):
            for j in range(self.colunas):
                if self.campo_minado[i, j] == self.bomba:
                    self.campo[i, j] = self.bomba

    def sem_bomba(self, linha, coluna):
        ja_vistos = np.array([], dtype=int)
        nao_vistos = self.redondezas(linha, coluna)
        nao_vistos = nao_vistos.reshape((-1, 2))
        # print(nao_vistos)
        # print('-')

        while nao_vistos.any():
            for posicao in nao_vistos:
                incluido_ja_vistos = self.contido(posicao, ja_vistos)

                elemento = self.campo_minado[posicao[0], posicao[1]]
                if int(elemento) == 0 and not incluido_ja_vistos:
                    provisorio = self.redondezas(posicao[0], posicao[1]).reshape((-1, 2))
                    incluido_provisorio = self.interseccao(provisorio, nao_vistos, interseccao=False)

                    if incluido_provisorio.any():
                        nao_vistos = np.append(nao_vistos, incluido_provisorio)
                        nao_vistos = nao_vistos.reshape((-1, 2))

                ja_vistos = np.append(ja_vistos, posicao)
                ja_vistos = ja_vistos.reshape((-1, 2))

            ja_vistos = ja_vistos.reshape((-1, 2))
            nao_vistos = np.delete(nao_vistos, 0, axis=0)

        return ja_vistos

    @staticmethod
    def contido(elemento, array):
        for item in array:
            if (elemento == item).all():
                return True
        return False

    @classmethod
    def interseccao(cls, array1, array2, interseccao=True):
        intersec = list(filter(lambda x: x in array1.tolist(), array2.tolist()))
        if interseccao:
            return np.array(intersec).reshape((-1, 2)).astype(int)

        else:
            not_intersec = array1.tolist()
            for i in range(len(intersec)):
                del not_intersec[not_intersec.index(intersec[i])]
            return np.array(not_intersec).reshape((-1, 2)).astype(int)
