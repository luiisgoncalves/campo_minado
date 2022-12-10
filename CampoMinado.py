import numpy as np
from time import time
from Campo import Campo
from random import randint
from Log import Log


class CampoMinado(Campo):
    def __init__(self,
                 linhas: int,
                 colunas: int,
                 dificulade: float,
                 log: Log,
                 elemento: str = '·',
                 bomba: str = 'X',
                 marcacao: str = 'ß',
                 duvida: str = '?',
                 marcacao_errada: str = 'E',
                 bomba_explosao: str = 'Q'):
        """metodo de inicializacao da classe Campo Minado sendo herdada da classe Campo"""
        super().__init__(linhas, colunas, log, elemento)  # chama o inicializador da superclasse Campo
        self._dificuldade = dificulade
        self._bomba = bomba
        self._marcacao = marcacao
        self._qntd_marcacoes = 0
        self._duvida = duvida
        self._marcacao_errada = marcacao_errada
        self._bomba_explosao = bomba_explosao
        self.campo_minado = np.copy(self.campo)
        self.posicoes = self.linhas * self.colunas
        self._quantidade_bombas = int(self.posicoes * self._dificuldade)
        self.inicio = time()
        self.bombas = []
        self.cria_bombas()
        self.conta_bombas()
        self.log.log[14] = self._dificuldade  # LOG

    def cria_bombas(self) -> None:
        """metodo responsavel pela criacao das bombas de forma aleatoria"""
        i = 0
        while i < self._quantidade_bombas:
            posicao_bomba = randint(0, self.posicoes - 1)
            if posicao_bomba not in self.bombas:
                self.bombas.append(posicao_bomba)
                i += 1

        # caso queria ver a quantidade e posicao de todas as bombas
        #############################################################
        # print(len(self.bombas))
        # self.bombas.sort()
        # print(self.bombas)
        #############################################################

        self.adiciona_bombas()

    def adiciona_bombas(self) -> None:
        """metodo responsavel por adicionar todas as bombas no campo minado"""
        for bomba in self.bombas:
            linha = bomba // self.colunas
            coluna = bomba % self.colunas
            self.campo_minado[linha][coluna] = self._bomba

    def conta_bombas(self) -> None:
        """metodo responsavel por verificar quantas bombas estao ao redor de cada elemento do campo minado"""
        for linha in range(self.linhas):
            for coluna in range(self.colunas):

                matriz_index = self.redondezas(linha, coluna)

                if self.campo_minado[linha][coluna] != self._bomba:
                    qntd_bomba = 0
                    for item in matriz_index:
                        line, column = item
                        if 0 <= line < self.linhas and 0 <= column < self.colunas:
                            qntd_bomba = qntd_bomba + 1 if self.campo_minado[line][column] == self._bomba else qntd_bomba
                    self.campo_minado[linha][coluna] = qntd_bomba

    def ver_elementos(self, linha: int, coluna: int) -> np.ndarray:
        """recebe a linha e posicao de um elemento do campo minado e retorna uma submatriz 3x3 contendo todos os elementos que estao nas redondezas do elemento passado"""

        # nao estou usando este metodo em nenhuma parte do meu programa!!!
        # provavelmente criei no inicio e mais tarde vi que nao tinha mais necessidade de usa-la, mas nao quis excluir

        matriz = self.redondezas(linha, coluna)
        sub_matriz = np.array([], dtype=int)

        for elemento in matriz:
            if 0 <= elemento[0] < self.linhas and 0 <= elemento[1] < self.colunas:
                item = int(self.campo_minado[elemento[0], elemento[1]]) if self.campo_minado[elemento[0], elemento[1]] != self._bomba else -1
                sub_matriz = np.append(sub_matriz, item)

        #  as proximas linhas serão responsaveis por fazer o reshape da submatriz conforme a sua quantidade de elementos
        match len(sub_matriz):                                          # verifica a quantidade de elementos da submatriz
            case 4:                                                     # caso tenha quatro elementos, quer dizer que o elemento passado de entrada esta em um dos cantos do campo minado
                sub_matriz = sub_matriz.reshape((2, 2))                 # faz um reshape na submatriz para ficar com duas linhas e duas colunas
            case 6:                                                     # caso tenha seis elementos, quer dizer que o elemento passado de entrada esta em um dos lados do campo minado
                if matriz[0, 1] == -1 or matriz[9, 1] == self.colunas:  # verificar se o elemento esta em uma das laterais
                    sub_matriz = sub_matriz.reshape((3, 2))             # faz um reshape na submatriz para ficar com tres linhas e duas colunas
                else:                                                   # caso nao esteja, significa que esta na parte superior ou inferior
                    sub_matriz = sub_matriz.reshape((2, 3))             # faz um reshape na submatriz para ficar com duas linhas e tres colunas
            case 9:                                                     # caso tenha nove elementos, quer dizer que o elemento passado de entrada esta em alguma parte do meio do campo minado
                sub_matriz = sub_matriz.reshape((3, 3))                 # faz um reshape na submatriz para ficar com tres linhas e tres colunas

        return sub_matriz

    def redondezas(self, linha: int, coluna: int) -> np.ndarray:
        """responsavel por verificar todos os indices dos elementos que estao nas redondezas do elemento com linha e coluna passados como entrada"""
        dimensao = (-1, 0, 1)
        matriz_index = np.array([], dtype=int)

        # outra forma de encontrar os elementos das redondezas
        # (prefiro esta solucao, mas existe algum erro de codigo que eu nao quis procurar nesta versao)
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

                if 0 <= line < self.linhas and 0 <= column < self.colunas:  # se tanto a linha quanto a coluna estão dentro das dimensoes do campo
                    matriz_index = np.append(matriz_index, [line, column])
        return matriz_index.reshape((-1, 2))

    def escolha(self, linha: int, coluna: int) -> bool:
        """recebe uma linha e uma coluna e verifica se esta posicao contem ou nao uma bomba no campo minado"""
        if self.campo_minado[linha, coluna] == self._bomba and self.campo[linha, coluna] != self._marcacao:
            self.log.log[2] += 1  # LOG
            self.explosao()
            self.campo[linha, coluna] = self._bomba_explosao
            return True
        else:
            self.verifica_local_livre(linha, coluna)
            return False

    def verifica_local_livre(self, linha: int, coluna: int) -> None:
        """verifica se a posicao passada eh uma posicao livre ou se existe bomba nas redondezas"""
        self.log.log[2] += 1 if self.campo[linha, coluna] == self._elemento else 0  # LOG
        self.log.log[2] += 1 if self.campo[linha, coluna] == self._duvida else 0    # LOG

        if self.campo[linha, coluna] == self.marcacao:
            pass

        elif int(self.campo_minado[linha, coluna]) == 0:  # se a posicao passada for zero, significa que nao existem bombas nas redondezas
            livres = self.sem_bomba(linha, coluna)        # chama o metodo sem_bomba que retorna numpy.ndarray com todos os elementos que serão revelados ao jogador
            for livre in livres:
                line, column = livre
                if self.campo[line, column] == str(self._marcacao):
                    continue
                self.campo[line, column] = int(self.campo_minado[line, column])

        else:  # caso contrário, significa que existe uma bomba nas redondezas e apenas este elemento será revelado
            self.campo[linha, coluna] = int(self.campo_minado[linha, coluna])

    def explosao(self) -> None:
        """responsavel por mostrar todas as bombas contidas no campo minado ao usuario.
        chamada nas vezes em que o jogador selecionou um local que contem uma bomba"""
        for i in range(self.linhas):
            for j in range(self.colunas):
                if self.campo_minado[i, j] == self._bomba and self.campo[i, j] != self.marcacao:
                    self.campo[i, j] = self._bomba
                elif self.campo[i, j] == self.marcacao and self.campo_minado[i, j] != self._bomba:
                    self.campo[i, j] = self._marcacao_errada
                    self.log.log[4] -= 1             # LOG
                    self.log.log[5] += 1             # LOG
        self.log.log[3] = np.sum(self.log.log[4:6])  # LOG

    def sem_bomba(self, linha: int, coluna: int) -> np.ndarray:
        """recebe a linha e coluna correspondentes de um elemento do campo minado e retorna uma lista com todos os elementos das redondezas que nao contem bombas"""
        ja_vistos = np.empty(0, dtype=int)                                # array que contera todos os elementos ja vistos
        nao_vistos = self.redondezas(linha, coluna)                       # array contendo todos os elementos ainda nao vistos

        while nao_vistos.any():                                           # se ainda existir algum elemento no array nao_vistos
            for posicao in nao_vistos:                                    # olhar para cada elemento do array nao_vistos
                incluido_ja_vistos = self.contido(posicao, ja_vistos)     # variavel verificadora se o elemento ja foi visto

                elemento = self.campo_minado[posicao[0], posicao[1]]      # variavel contendo o elemento atual correspondente no campo minado
                if int(elemento) == 0 and not incluido_ja_vistos:         # caso o elemento atual seja zero e o seu indice nao tenha sido visto ainda
                    provisorio = self.redondezas(posicao[0], posicao[1])  # variavel provisoria que armazenara todos os elementos das redondezas da atual posicao que esta sendo verificada
                    incluido_provisorio = self.not_interseccao(provisorio, nao_vistos)            # variavel que armazena todos os elementos da variavel provisorio que ainda nao foram verificados

                    if incluido_provisorio.any():                                                 # se tiver algum novo elemento que ainda nao foi verificado
                        nao_vistos = np.append(nao_vistos, incluido_provisorio).reshape((-1, 2))  # todos os novos elementos novos que ainda nao foram vistos sao armazenados na variavel nao_vistos
                ja_vistos = np.append(ja_vistos, posicao).reshape((-1, 2))                        # elemento que acabou de ser tratado eh armazenado na variavel ja_vistos, para nao ser consultado novamente
                nao_vistos = np.delete(nao_vistos, 0, axis=0)                                     # o mesmo elemento tambem eh excluido da lista de elementos que ainda nao foram vistos
        return ja_vistos                                                                          # retorna todos os elementos que serão revelados no campo

    def qtd_posicoes_disponiveis(self) -> int:
        """retorna a quantidade de posições que o jogador ainda pode selecionar"""
        elementos = [self._elemento, self._marcacao, self._duvida]
        qntd_posicoes = 0

        for linha in range(self.linhas):
            for coluna in range(self.colunas):
                if self.campo[linha, coluna] in elementos:
                    qntd_posicoes += 1

        return qntd_posicoes

    def sinalizacao(self, linha, coluna) -> None:
        """responsavel por adicionar (ou remover) uma bandeira ou duvida no campo passada uma linha e coluna"""
        if self.campo[linha, coluna] == self.elemento:
            self.campo[linha, coluna] = self._marcacao
            self._qntd_marcacoes += 1
            self.log.log[4] += 1  # LOG
        elif self.campo[linha, coluna] == self._marcacao:
            self.campo[linha, coluna] = self._duvida
            self._qntd_marcacoes -= 1
            self.log.log[4] -= 1  # LOG
            self.log.log[6] += 1  # LOG
        elif self.campo[linha, coluna] == self._duvida:
            self.campo[linha, coluna] = self.elemento
            self.log.log[6] -= 1  # LOG

    @staticmethod
    def contido(elemento: np.ndarray, array: np.ndarray) -> bool:
        """verifica se um certo elemento esta contido no array passado"""
        for item in array:
            if (elemento == item).all():
                return True
        return False

    @classmethod
    def not_interseccao(cls, array1, array2) -> np.ndarray:
        """retornar todos os elementos do array1 que NAO estao contidos no array2
        numpy.ndarray, numpy.ndarray -> numpy.ndarray"""
        intersec = list(filter(lambda x: x in array1.tolist(), array2.tolist()))
        not_intersec = array1.tolist()
        for i in range(len(intersec)):
            del not_intersec[not_intersec.index(intersec[i])]
        return np.array(not_intersec).reshape((-1, 2)).astype(int)

    @property
    def bomba(self):
        return self._bomba

    @property
    def marcacao(self):
        return self._marcacao

    @property
    def duvida(self):
        return self._duvida

    @property
    def qtd_bombas(self):
        return self._quantidade_bombas

    @property
    def dificuldade(self):
        return self._dificuldade

    @property
    def marcacao_errada(self):
        return self._marcacao_errada

    @property
    def bomba_explosao(self):
        return self._bomba_explosao

    @property
    def qntd_marcacoes(self):
        return self._qntd_marcacoes
