import pygame
from Cenario import Cenario
from Game import Game


def jogo_no_terminal():
    jogo = True

    while jogo:
        game = Game(terminal=True)
        jogo = game.game()


def main():
    # enquanto nao crio um menu, unico modo de alterar as configuracoes eh diretamente pela linha de codigo abaixo
    cenario = Cenario(20, 20, 0.1)

    while True:
        cenario.processar_eventos(pygame.event.get())
        cenario.contagem_tempo()
        pygame.display.update()


if __name__ == '__main__':
    # main()
    jogo_no_terminal()
