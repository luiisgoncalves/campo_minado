import numpy
import numpy as np
from random import randint, seed

seed(47)  # fixme: seed utilizada para padronizar os testes (no codigo final esta linha deve ser apagada para garantir a pseudoaleatoriedade)


class Campo:
    def __init__(self, linhas: int, colunas: int, elemento: str = '·'):
        """funcao de inicializacao da classe Campo.
        cria a quantidade de linhas, colunas os elementos neutros (ja com valor default) e o ndarray que representa a matriz do campo vazio
        int, int, str -> None"""
        self.linhas = linhas
        self.colunas = colunas
        self.elemento = elemento
        self.campo = np.full((linhas, colunas), elemento)

    def mostra_campo(self, campo_minado: list | numpy.ndarray | None = None, espacamento: str = '   '):
        """funcao responsavel por mostrar o campo no estado atual
        list, str -> None"""
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
    def __init__(self, linhas: int, colunas: int, dificulade: float, elemento: str = '·', bomba: str = 'X', marcacao: str = 'ß', duvida: str = '?'):
        """funcao de inicializacao da classe Campo Minado sendo herdada da classe Campo.
        int, int, float, str, str, str, str -> None"""
        super().__init__(linhas, colunas, elemento)  # chama o inicializador da superclasse Campo
        self.dificuldade = dificulade
        self.bomba = bomba
        self.marcacao = marcacao
        self.duvida = duvida
        self.campo_minado = np.copy(self.campo)
        self.posicoes = self.linhas * self.colunas
        self.quantidade_bombas = int(self.posicoes * self.dificuldade)
        self.bombas = []

    def cria_bombas(self):
        """funcao responsavel pela criacao das bombas de forma aleatoria
        None -> None"""
        i = 0
        while i < self.quantidade_bombas:
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

    def adiciona_bombas(self):
        """funcao responsavel por adicionar todas as bombas no campo minado
        None -> None"""
        for bomba in self.bombas:
            linha = bomba // self.colunas
            coluna = bomba % self.colunas
            self.campo_minado[linha][coluna] = self.bomba

    def conta_bombas(self):
        """funcao responsavel por verificar quantas bombas estao ao redor de cada elemento do campo minado
        None -> None"""
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

    def ver_elementos(self, linha: int, coluna: int):
        """recebe a linha e posicao de um elemento do campo minado e retorna uma submatriz 3x3 contendo todos os elementos que estao nas redondezas do elemento passado
        int, int -> numpy.ndarray"""

        # nao estou usando esta funcao em nenhuma parte do meu programa!!!
        # provavelmente criei no inicio e mais tarde vi que nao tinha mais necesseidade de usa-la, mas nao quis excluir

        matriz = self.redondezas(linha, coluna)
        sub_matriz = np.array([], dtype=int)

        for elemento in matriz:
            if 0 <= elemento[0] < self.linhas and 0 <= elemento[1] < self.colunas:
                item = int(self.campo_minado[elemento[0], elemento[1]]) if self.campo_minado[elemento[0], elemento[1]] != self.bomba else -1
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

    def redondezas(self, linha: int, coluna: int):
        """responsavel por verificar todos os indices dos elementos que estao nas redondezas do elemento com linha e coluna passados como entrada
        int, int -> numpy.ndarray"""
        dimensao = (-1, 0, 1)
        matriz_index = np.array([], dtype=int)

        # outra forma de encontrar os elementos das redondezas (existe algum erro que eu nao quis procurar)
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

    def escolha(self, linha: int, coluna: int):
        """recebe uma linha e uma coluna e verifica se esta posicao contem ou nao uma bomba no campo minado
        int, int -> bool"""
        if self.campo_minado[linha, coluna] == self.bomba:
            self.explosao()
            return True
        else:
            self.verifica_local_livre(linha, coluna)
            return False

    def verifica_local_livre(self, linha: int, coluna: int):
        """verifica se a posicao passada eh uma posicao livre ou se existe bomba nas rendondezas
        int, int -> None"""
        if int(self.campo_minado[linha, coluna]) == 0:  # se a posicao passada for zero, significa que nao existem bombas nas redondezas
            livres = self.sem_bomba(linha, coluna)      # chama a funcao sem_bomba que retorna numpy.ndarray com todos os elementos que serão revelados ao jogador
            for livre in livres:
                line, column = livre
                self.campo[line, column] = self.campo_minado[line, column]
        else:  # caso contrário, significa que existe uma bomba nas redondezas e apenas este elemento será revelado
            self.campo[linha, coluna] = self.campo_minado[linha, coluna]

    def explosao(self):
        """responsavel por mostrar todas as bombas contidas no campo minado ao usuario.
        chamada nas vezes em que o jogador selecionou um local que contem uma bomba
        None -> None"""
        for i in range(self.linhas):
            for j in range(self.colunas):
                if self.campo_minado[i, j] == self.bomba:
                    self.campo[i, j] = self.bomba

    def sem_bomba(self, linha: int, coluna: int):
        """recebe a linha e coluna correspondentes de um elemento do campo minado e retorna uma lista com todos os elementos das redondezas que nao contem bombas
        int, int -> numpy.ndarray"""
        ja_vistos = np.array([], dtype=int)                               # array que conterah todos os elementos ja vistos
        nao_vistos = self.redondezas(linha, coluna)                       # array contendo todos os elementos ainda nao vistos

        while nao_vistos.any():                                           # se ainda existir algum elemento no array nao_vistos
            for posicao in nao_vistos:                                    # olhar para cada elemento do array noa_vistos
                incluido_ja_vistos = self.contido(posicao, ja_vistos)     # variavel verificadora se o elemento ja foi visto

                elemento = self.campo_minado[posicao[0], posicao[1]]      # variavel contendo o elemento atual correspondente no campo minado
                if int(elemento) == 0 and not incluido_ja_vistos:         # caso o elemento atual seja zero e o seu indice nao tenha sido visto ainda
                    provisorio = self.redondezas(posicao[0], posicao[1])  # variavel provisoria que armazenara todos os elementos das redondezas da atual posicao que esta sendo verificada
                    incluido_provisorio = self.not_interseccao(provisorio, nao_vistos)            # variavel que armazena todos os elementos da variavel provisorio que ainda nao foram verificados

                    if incluido_provisorio.any():                                                 # se tiver algum novo elemento que ainda nao foi verificado
                        nao_vistos = np.append(nao_vistos, incluido_provisorio).reshape((-1, 2))  # todos os novos elementos novos que ainda nao foram vistos sao armazenados na variavel nao_vistos
                ja_vistos = np.append(ja_vistos, posicao).reshape((-1, 2))                        # elemento que acabou de ser tratado eh armazenado na variavel ja_vistos, para nao ser consultado novamente
                nao_vistos = np.delete(nao_vistos, 0, axis=0)                                     # o mesmo elemento tambem eh excluido da lista de elementos que ainda nao foram vistos

        return ja_vistos  # retorna todos os elementos que serão revelados no campo

    def qntd_posicoes_disponiveis(self):
        """retorna a quantidade de posições que o jogador ainda pode selecionar
        None -> int"""
        elementos = [self.elemento, self.marcacao, self.duvida]
        qntd_posicoes = 0

        for linha in range(self.linhas):
            for coluna in range(self.colunas):
                if self.campo[linha, coluna] in elementos:
                    qntd_posicoes += 1
        return qntd_posicoes

    @staticmethod
    def contido(elemento: numpy.ndarray, array: numpy.ndarray):
        """verifica se um certo elemento esta contido no array passado
        numpy.ndarray, numpy.ndarray -> numpy.ndarray"""
        for item in array:
            if (elemento == item).all():
                return True
        return False

    @classmethod
    def interseccao(cls, array1, array2):
        """retorna todos os elementos que estao contidos tanto no array1 quanto no array2
        numpy.ndarray, numpy.ndarray -> numpy.ndarray"""
        intersec = list(filter(lambda x: x in array1.tolist(), array2.tolist()))
        return np.array(intersec).reshape((-1, 2)).astype(int)

    @classmethod
    def not_interseccao(cls, array1, array2):
        """retornar todos os elementos do array1 que NAO estao contidos no array2
        numpy.ndarray, numpy.ndarray -> numpy.ndarray"""
        intersec = list(filter(lambda x: x in array1.tolist(), array2.tolist()))
        not_intersec = array1.tolist()
        for i in range(len(intersec)):
            del not_intersec[not_intersec.index(intersec[i])]
        return np.array(not_intersec).reshape((-1, 2)).astype(int)
