import pygame
from Cenario import Cenario
from Game import Game
from random import seed

seed(47)  # TODO: nao esquecer de remover a semente para voltar ficar criando cenarios pseudoaleatorios


def jogo_no_terminal() -> None:
    """doc"""
    jogo = True

    while jogo:
        jogo = Game().game()
        jogo = True if jogo is None else jogo


def main() -> None:
    """doc"""
    # enquanto nao crio um menu, unico modo de alterar as configuracoes eh diretamente pela linha de codigo abaixo
    cenario = Cenario(20, 20, 0.1)

    while True:
        cenario.processar_eventos(pygame.event.get())
        cenario.contagem_tempo()
        pygame.display.update()


if __name__ == '__main__':
    # main()
    jogo_no_terminal()
