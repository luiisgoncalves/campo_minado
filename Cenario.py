from CampoMinado import CampoMinado
from Log import Log
from constantes import *
import pygame
import time

pygame.init()
fonte = pygame.font.SysFont('arial', 32, True, False)
pygame.display.set_icon(BOMBA)
pygame.display.set_caption('Minesweeper')


class Cenario:  # classe responsavel pela criacao do cenario do jogo e das interacoes com o jogador
    def __init__(self, linhas, colunas, dificuldade):
        self.linhas = linhas                                            # quantidade de linhas do campo minado
        self.colunas = colunas                                          # quantidade de colunas do campo minado
        self.log = Log()
        self.log.start()
        self.largura_tela = self.colunas * ESCALA_MENOR[0]              # largura da tela que será gerada
        self.altura_tela = self.linhas * ESCALA_MENOR[1]                # altura da tela que será gerada
        self.campo_minado_ = CampoMinado(linhas, colunas, dificuldade, self.log)  # criacao de uma instacia da classe CampoMinado
        self.campo_minado_.log.log[15] = 1
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

        x_pos, y_pos = pygame.mouse.get_pos()     # pega a posicao atual o mouse

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
        self.pinta_campo()
        self.pintar_game_over()
        self.screen.blit(BOTAO_DERROTA, self.posicao_botao())

    def venceu(self) -> None:
        """trata o cenario em que o jogador venceu a partida"""
        self.start = False
        self.vitoria = True
        self.pinta_campo()
        self.pintar_vitoria()
        self.screen.blit(BOTAO_VITORIA, self.posicao_botao())

    def verifica_escolha(self, line: int, column: int) -> None:
        """verifica se o jogador venceu ou perdeu a partida"""
        derrota = self.campo_minado_.escolha(line, column)
        if derrota:
            self.perdeu()
            return

        vitoria = self.campo_minado_.qtd_posicoes_disponiveis() == self.campo_minado_.qtd_bombas
        if vitoria:
            self.venceu()
            return

        self.pinta_campo()

    def processar_eventos(self, eventos: list) -> None:
        """metodo que processara os eventos gerados pelo usuario (cliques do mouse)"""
        for e in eventos:
            if e.type == pygame.QUIT:  # se o jogador fechou a tela do jogo o programa encerra
                if self.start:
                    self.campo_minado_.log.log[11] = 1
                    self.campo_minado_.log.save()  # LOG
                exit()

            elif e.type == pygame.MOUSEBUTTONDOWN:          # se o jogador apertou um dos botoes do mouse...
                line, column = self.busca_linha_e_coluna()  # ...verifica a linha e coluna baseado no tamanho dos quadrados do campo minado

                if e.button == ESQUERDO:
                    #  eu defini como linha zero a primeira fileira dos quadrados e, como existe uma margem na parte superior (onde fica os digitos de contagem e o botao central), por isso existe a possibilidade do jogador clicar em uma 'linha negativa'
                    if line >= 0 and not self.derrota and not self.vitoria:
                        self.inicia_tempo()
                        self.verifica_escolha(line, column)

                    elif self.botao_apertado():  # verifica se o jogador apertou o botao de reinicio
                        self.screen.blit(BOTAO_PRESSIONADO, self.posicao_botao())
                        self.soltou = True
                        if self.start:
                            self.campo_minado_.log.log[10] = 1  # LOG
                            self.campo_minado_.log.save()  # LOG

                elif e.button == DIREITO:  # insercao, ou remocao, das bandeiras e duvidas
                    self.campo_minado_.sinalizacao(line, column)
                    if line >= 0 and not self.derrota and not self.vitoria:
                        self.pinta_qntd_bomba()
                        self.pinta_campo()

            elif e.type == pygame.MOUSEBUTTONUP and e.button == ESQUERDO and self.soltou:  # realizar esta acao apenas quando o jogador SOLTOU o botao de reinicio
                # reinicializa quase todos os atributos para uma nova partida
                self.log = Log()
                self.campo_minado_ = CampoMinado(self.linhas, self.colunas, self.campo_minado_.dificuldade, self.log)
                self.campo_minado_.log.start()
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
        qntd = self.campo_minado_.qtd_bombas - self.campo_minado_.qntd_marcacoes
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
