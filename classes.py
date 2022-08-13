from random import randint
from constantes import *
import numpy as np
import pygame
import time

pygame.init()
fonte = pygame.font.SysFont('arial', 32, True, False)
pygame.display.set_icon(BOMBA)
pygame.display.set_caption('Minesweeper')


class Campo:
    def __init__(self, linhas: int, colunas: int, elemento: str = '·') -> None:
        """metodo de inicializacao da classe Campo.
        cria a quantidade de linhas, colunas os elementos neutros (ja com valor default) e o ndarray que representa a matriz do campo vazio"""
        self.linhas = linhas
        self.colunas = colunas
        self._elemento = elemento
        self.campo = np.full((self.linhas, self.colunas), self._elemento)

    def mostra_campo(self, campo_minado: list | np.ndarray | None = None, espacamento: str = '   ') -> None:
        """metodo responsavel por mostrar o campo no estado atual"""
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

    @property
    def elemento(self) -> str:
        return self._elemento


class CampoMinado(Campo):
    def __init__(self,
                 linhas: int,
                 colunas: int,
                 dificulade: float,
                 elemento: str = '·',
                 bomba: str = 'X',
                 marcacao: str = 'ß',
                 duvida: str = '?',
                 marcacao_errada: str = 'E',
                 bomba_explosao: str = 'Q'):
        """metodo de inicializacao da classe Campo Minado sendo herdada da classe Campo"""
        super().__init__(linhas, colunas, elemento)  # chama o inicializador da superclasse Campo
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
        self.bombas = []
        self.cria_bombas()
        self.conta_bombas()

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
        # provavelmente criei no inicio e mais tarde vi que nao tinha mais necesseidade de usa-la, mas nao quis excluir

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

    def escolha(self, linha: int, coluna: int) -> bool:
        """recebe uma linha e uma coluna e verifica se esta posicao contem ou nao uma bomba no campo minado"""
        if self.campo_minado[linha, coluna] == self._bomba and self.campo[linha, coluna] != self._marcacao:
            self.explosao()
            self.campo[linha, coluna] = self._bomba_explosao
            return True
        else:
            self.verifica_local_livre(linha, coluna)
            return False

    def verifica_local_livre(self, linha: int, coluna: int) -> None:
        """verifica se a posicao passada eh uma posicao livre ou se existe bomba nas rendondezas"""
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

    def sem_bomba(self, linha: int, coluna: int) -> np.ndarray:
        """recebe a linha e coluna correspondentes de um elemento do campo minado e retorna uma lista com todos os elementos das redondezas que nao contem bombas"""
        ja_vistos = np.array([], dtype=int)                               # array que conterah todos os elementos ja vistos
        nao_vistos = self.redondezas(linha, coluna)                       # array contendo todos os elementos ainda nao vistos

        while nao_vistos.any():                                           # se ainda existir algum elemento no array nao_vistos
            for posicao in nao_vistos:                                    # olhar para cada elemento do array noa_vistos
                incluido_ja_vistos = self.contido(posicao, ja_vistos)     # variavel verificadora se o elemento ja foi visto

                elemento = self.campo_minado[posicao[0], posicao[1]]      # variavel contendo o elemento atual correspondente no campo minado
                # print(elemento)
                if int(elemento) == 0 and not incluido_ja_vistos:         # caso o elemento atual seja zero e o seu indice nao tenha sido visto ainda
                    provisorio = self.redondezas(posicao[0], posicao[1])  # variavel provisoria que armazenara todos os elementos das redondezas da atual posicao que esta sendo verificada
                    incluido_provisorio = self.not_interseccao(provisorio, nao_vistos)            # variavel que armazena todos os elementos da variavel provisorio que ainda nao foram verificados

                    if incluido_provisorio.any():                                                 # se tiver algum novo elemento que ainda nao foi verificado
                        nao_vistos = np.append(nao_vistos, incluido_provisorio).reshape((-1, 2))  # todos os novos elementos novos que ainda nao foram vistos sao armazenados na variavel nao_vistos
                ja_vistos = np.append(ja_vistos, posicao).reshape((-1, 2))                        # elemento que acabou de ser tratado eh armazenado na variavel ja_vistos, para nao ser consultado novamente
                nao_vistos = np.delete(nao_vistos, 0, axis=0)                                     # o mesmo elemento tambem eh excluido da lista de elementos que ainda nao foram vistos
        return ja_vistos  # retorna todos os elementos que serão revelados no campo

    def qntd_posicoes_disponiveis(self) -> int:
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
        elif self.campo[linha, coluna] == self._marcacao:
            self.campo[linha, coluna] = self._duvida
            self._qntd_marcacoes -= 1
        elif self.campo[linha, coluna] == self._duvida:
            self.campo[linha, coluna] = self.elemento

    @staticmethod
    def contido(elemento: np.ndarray, array: np.ndarray) -> bool:
        """verifica se um certo elemento esta contido no array passado"""
        for item in array:
            if (elemento == item).all():
                return True
        return False

    @classmethod
    def interseccao(cls, array1, array2) -> np.ndarray:
        """retorna todos os elementos que estao contidos tanto no array1 quanto no array2
        numpy.ndarray, numpy.ndarray -> numpy.ndarray"""
        intersec = list(filter(lambda x: x in array1.tolist(), array2.tolist()))
        return np.array(intersec).reshape((-1, 2)).astype(int)

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
    def quantidade_bombas(self):
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


class Cenario:  # classe responsavel pela criacao do cenario do jogo e das interacoes com o jogador
    def __init__(self, linhas, colunas, dificuldade):
        self.linhas = linhas                                            # quantidade de linhas do campo minado
        self.colunas = colunas                                          # quantidade de colunas do campo minado
        self.largura_tela = self.colunas * ESCALA_MENOR[0]              # largura da tela que será gerada
        self.altura_tela = self.linhas * ESCALA_MENOR[1]                # altura da tela que será gerada
        self.campo_minado_ = CampoMinado(linhas, colunas, dificuldade)  # criacao de uma instacia da classe CampoMinado
        self.screen = self.cria_tela()                                  # chama o metodo que criara a tela do jogo
        self.x_pos_qntd_bomba = 0  # posicao horizontal inicial onde será pintada na tela as imagens do digitos referentes à quantidade de bombas restantes para o jogador descobrir
        self.y_pos_qntd_bomba = 0  # posicao vertical inicial onde será pintada na tela as imagens do digitos referentes à quantidade de bombas restantes para o jogador descobrir
        self.x_pos_tempo = self.screen.get_width() - (ESCALA_MEDIA[0] * 3)  # posicao horizontal inicial onde será pintada na tela as imagens do digitos referentes ao tempo de jogo
        self.y_pos_tempo = 0       # posicao vertical inicial onde será pintada na tela as imagens do digitos referentes ao tempo de jogo
        self.pinta_tela()          # chama o metodo que, de fato pintara, a tela do jogo
        self.pinta_botao()         # chama o metodo que pintara o botao de reinicio do jogo
        self.pinta_qntd_bomba()    # chama o metodo que pintara os digitos (canto superior esquerdo) que indicam a quantidade de bombas ja marcadas
        self.inicio = 0            # atributo que armazera o horario que o jogador iniciou a partida
        self.start = False         # atributo responsavel por iniciar a contagem de tempo da partida
        self.soltou = False        # atributo para verificar se o jogador soltou o botao (central) de reinicio da partida
        self.derrota = False       # atributo responsavel informar se o jogador perdeu a partida
        self.vitoria = False       # atributo responsavel informar se o jogador venceu a partida

    def cria_tela(self) -> pygame.Surface:
        """cria e retorna um objeto do tipo Surface do pygame que será usado para criacao da tela do jogo"""
        screen = pygame.display.set_mode((self.largura_tela, MARGEM_SUPERIOR + self.altura_tela))
        return screen

    def contagem_tempo(self) -> None:
        """responsavel por chamar o metodo que pintara o relogio do jogo com o tempo ja decorrido desde o início da partida"""
        if not self.derrota and not self.vitoria and self.start:  # so chama o metodo se o jogador nao ganhou, nao perdeu e se ele iniciou a partida
            self.pinta_tempo()

    def inicia_tempo(self) -> None:
        """responsavel por indicar que a partida comecou e marcar o horario de início da mesma"""
        if not self.start:
            self.start = True
            self.inicio = time.time()

    def botao_apertado(self) -> bool:
        """verifica se o jogador clicou no botao de reinicio (central)"""
        lat_esq, superior = self.posicao_botao()  # pega a lateral esquerda e a parte superior do botao
        lat_dir = lat_esq + ESCALA_MAIOR[0]       # pega a lateral direita do botao
        inferior = superior + ESCALA_MAIOR[1]     # pega a parte inferior do botao

        x_pos, y_pos = pygame.mouse.get_pos()     # pega a bosicao atual o mouse

        # verifica se o mouse clicou no quadrado que o botao esta posicionado na tela
        if lat_esq <= x_pos <= lat_dir and superior <= y_pos <= inferior:
            return True
        return False

    def posicao_botao(self) -> tuple[int, int]:
        """retorna a posicao (ponta superior esquerda) que sera gerada a imagem do botao de reinicio"""
        return (self.largura_tela // 2) - (ESCALA_MAIOR[0] // 2), 0

    def perdeu(self) -> None:
        """trata o cenario em que o jogador perdeu a partida"""
        self.start = False
        self.derrota = True
        self.pintar_game_over()
        self.screen.blit(BOTAO_DERROTA, self.posicao_botao())

    def venceu(self) -> None:
        """trata o cenario em que o jogador venceu a partida"""
        self.start = False
        self.vitoria = True
        self.pintar_vitoria()
        self.screen.blit(BOTAO_VITORIA, self.posicao_botao())

    def verifica_escolha(self, line: int, column: int) -> None:
        """verifica se o jogador venceu ou perdeu a partida"""
        derrota = self.campo_minado_.escolha(line, column)
        vitoria = self.campo_minado_.qntd_posicoes_disponiveis() == self.campo_minado_.quantidade_bombas
        self.pinta_campo()

        if derrota:
            self.perdeu()
        elif vitoria:
            self.venceu()

    def processar_eventos(self, eventos: list) -> None:
        """metodo que processara os eventos gerados pelo usuario (cliques do mouse)"""
        for e in eventos:
            if e.type == pygame.QUIT:  # se o jogador fechou a tela do jogo o programa encerra
                exit()

            elif e.type == pygame.MOUSEBUTTONDOWN:          # se o jogador apertou um dos botoes do mouse...
                line, column = self.busca_linha_e_coluna()  # ...verifica a linha e coluna baseado no tamanho dos quadrados do campo minado

                if e.button == ESQUERDO:
                    #  eu defini como linha zero a primeira fileira dos quadrados e, como existe uma margem na parte superior (onde fica os digitos de contagem e o botao central), por isso existe a possibilidade do jogador clicar em uma 'linha negativa'
                    if line >= 0 and not self.derrota and not self.vitoria:
                        self.verifica_escolha(line, column)
                        self.inicia_tempo()

                    elif self.botao_apertado():  # verifica se o jogador apertou o botao de reinicio
                        self.screen.blit(BOTAO_PRESSIONADO, self.posicao_botao())
                        self.soltou = True

                elif e.button == DIREITO:  # insercao, ou remocao, das bandeiras e duvidas
                    self.campo_minado_.sinalizacao(line, column)
                    if line >= 0 and not self.derrota and not self.vitoria:
                        self.pinta_qntd_bomba()
                        self.pinta_campo()

            elif e.type == pygame.MOUSEBUTTONUP and e.button == ESQUERDO and self.soltou:  # realizar esta acao apenas quando o jogador SOLTOU o botao de reinicio
                # reinicializa quase todos os atributos para uma nova partida
                self.campo_minado_ = CampoMinado(self.linhas, self.colunas, self.campo_minado_.dificuldade)
                self.screen.blit(BOTAO_DEFAULT, self.posicao_botao())
                self.screen = self.cria_tela()
                self.pinta_tela()
                self.pinta_botao()
                self.pinta_qntd_bomba()
                self.start = False
                self.soltou = False
                self.derrota = False
                self.vitoria = False

            # USADO PARA DESENVOLVIMENTO - VIZUALIZAR, NO TERMINAL, A POSICAO DE TODAS AS BOMBAS PARA REALIZA ALGUNS TESTES
            # elif e.type == pygame.KEYDOWN and e.key == pygame.K_p:
            #     self.campo_minado_.mostra_campo()

    def busca_elemento(self, linha: int, coluna: int) -> pygame.Surface:
        """retornar a imagem correspondente ao elemento da posicao [linha, coluna] do campo"""
        match self.campo_minado_.campo[linha, coluna]:
            case self.campo_minado_.elemento:
                return CAMPO_OCULTO
            case self.campo_minado_.bomba:
                return BOMBA
            case self.campo_minado_.bomba_explosao:
                return BOMBA_EXPLOSAO
            case self.campo_minado_.marcacao:
                return BANDEIRA
            case self.campo_minado_.duvida:
                return DUVIDA
            case self.campo_minado_.marcacao_errada:
                return BOMBA_ERRADA

        match int(self.campo_minado_.campo[linha, coluna]):
            case 0:
                return CAMPO_LIMPO
            case 1:
                return NUMEROS[1]
            case 2:
                return NUMEROS[2]
            case 3:
                return NUMEROS[3]
            case 4:
                return NUMEROS[4]
            case 5:
                return NUMEROS[5]
            case 6:
                return NUMEROS[6]
            case 7:
                return NUMEROS[7]
            case 8:
                return NUMEROS[8]

    @staticmethod
    def pega_posicao(linha: int, coluna: int) -> tuple[int, int]:
        """responsavel por receber a posicao da linha e coluna e retornar a posicao em píxeis para insercao das imagens"""
        linha *= ESCALA_MENOR[1]
        coluna *= ESCALA_MENOR[0]
        return coluna, linha + MARGEM_SUPERIOR

    @classmethod
    def busca_linha_e_coluna(cls) -> tuple[int, int]:
        """responsavel por pegar a posicao, em pixeis, do mouse e transformar em linhas e colunas para trabalhar com a matriz do campo minado"""
        # busca em que quadrado o mouse clicou
        coluna, linha = pygame.mouse.get_pos()
        coluna //= ESCALA_MENOR[1]
        linha = (linha - MARGEM_SUPERIOR) // ESCALA_MENOR[0]
        return linha, coluna

    # METODOS RESPONSAVEIS PELA PINTURA DOS CENARIOS E SITUACOES DO JOGO
    def pinta_tela(self) -> None:
        """pinta, na tela criada, os elementos iniciais do jogo"""
        self.screen.fill(GREY)  # tela criada com um background na cor cinza

        # pinta, no canto superior direito, os digitos de contagem de tempo zerados
        self.screen.blit(DIGITOS[0], (self.x_pos_tempo, self.y_pos_tempo))
        self.screen.blit(DIGITOS[0], (self.x_pos_tempo + ESCALA_MEDIA[0], self.y_pos_tempo))
        self.screen.blit(DIGITOS[0], (self.x_pos_tempo + ESCALA_MEDIA[0] * 2, self.y_pos_tempo))

        # pinta o campo minado
        for i in range(self.colunas):
            for j in range(self.linhas):
                self.screen.blit(CAMPO_OCULTO, (i * ESCALA_MENOR[0], MARGEM_SUPERIOR + j * ESCALA_MENOR[1]))

    def pinta_qntd_bomba(self) -> None:
        """responsavel por mostrar quantas bombas ainda restam para serem marcadas com bandeiras"""
        qntd = self.campo_minado_.quantidade_bombas - self.campo_minado_.qntd_marcacoes
        self.pinta_digitos(qntd, (self.x_pos_qntd_bomba, self.y_pos_qntd_bomba))

    def pinta_tempo(self) -> None:
        """responsavel por mostrar o relogio do jogo com o tempo ja decorrido desde o início da partida"""
        tempo = int(time.time() - self.inicio)  # verifica o horario atual menos o horario que a partida iniciou
        self.pinta_digitos(tempo, (self.x_pos_tempo, self.y_pos_tempo))

    def pinta_digitos(self, num: int, posicao: tuple) -> None:
        """responsavel por pintar os digitos na tela"""
        if num >= 0:
            # separacao das unidades, dezenas e centenas do numero recebido como entrada
            unidade = num % 10
            dezena = (num % 100) // 10
            centena = (num % 1000) // 100

            self.screen.blit(DIGITOS[centena], posicao)
            self.screen.blit(DIGITOS[dezena], (posicao[0] + ESCALA_MEDIA[0], posicao[1]))
            self.screen.blit(DIGITOS[unidade], (posicao[0] + ESCALA_MEDIA[0] * 2, posicao[1]))

        elif -99 <= num < 0:
            num *= -1  # transforma o numero em positivo apenas para facilitar nos calculos de separacao de unidades e dezenas
            unidade = num % 10
            self.screen.blit(DIGITOS[unidade], (posicao[0] + ESCALA_MEDIA[0] * 2, posicao[1]))

            if num < 10:
                self.screen.blit(DIGITOS[0], posicao)
                self.screen.blit(DIGITOS[-1], (posicao[0] + ESCALA_MEDIA[0], posicao[1]))
            else:
                dezena = (num % 100) // 10
                self.screen.blit(DIGITOS[-1], posicao)
                self.screen.blit(DIGITOS[dezena], (posicao[0] + ESCALA_MEDIA[0], posicao[1]))

        elif num < -99:
            self.screen.blit(DIGITOS[-1], posicao)
            self.screen.blit(DIGITOS[9], (posicao[0] + ESCALA_MEDIA[0], posicao[1]))
            self.screen.blit(DIGITOS[9], (posicao[0] + ESCALA_MEDIA[0] * 2, posicao[1]))

    def pinta_sinalizacao(self, linha: int, coluna: int) -> None:
        """responsavel por marcar, ou desmarcar, o quadrado com uma bandeira ou duvida"""
        self.screen.blit(self.busca_elemento(linha, coluna), self.pega_posicao(linha, coluna))

    def pinta_campo(self) -> None:
        """responsavel por pintar o estado atual do campo minado"""
        for i in range(self.linhas):
            for j in range(self.colunas):
                self.screen.blit(self.busca_elemento(i, j), self.pega_posicao(i, j))

    def pintar_texto_centro(self, texto: str) -> None:
        """responsavel por mostrar no centro da tela a mensagem de vitoria ou de derrota"""
        texto_img = fonte.render(texto, True, YELLOW)
        texto_x = (self.screen.get_width() - texto_img.get_width()) // 2
        texto_y = (self.screen.get_height() - texto_img.get_height()) // 2
        self.screen.blit(texto_img, (texto_x, texto_y))

    def pintar_vitoria(self) -> None:
        """responsavel por chamar o metodo de mostrar texto, passado mensagem de vitoria"""
        self.pintar_texto_centro('V I T O R I A ! ! !')

    def pintar_game_over(self) -> None:
        """responsavel por chamar o metodo de mostrar texto, passado mensagem de derrota"""
        self.pintar_texto_centro('G A M E R  O V E R')

    def pinta_botao(self) -> None:
        """responsavel por pintar o botao de reinicio de partida (botao central)"""
        self.screen.blit(BOTAO_DEFAULT, self.posicao_botao())
