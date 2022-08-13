from classes import CampoMinado, Cenario
import pygame
from functions import *


def jogo_no_terminal():
    jogo = True

    while jogo:
        lines, columns, difficulty = escolha_config()
        campo = CampoMinado(lines, columns, difficulty)
        campo.mostra_campo()

        partida = True
        while partida:
            line, column = escolha_posicao(lines, columns, campo)
            explosao = campo.escolha(line, column)
            campo.mostra_campo()

            if explosao:
                partida = False
                jogo = reinicio('perdeu! :(')

            elif campo.qntd_posicoes_disponiveis() == campo.quantidade_bombas:
                partida = False
                jogo = reinicio('ganhou!!!')


def main():
    # enquanto nao crio um menu, unico modo de alterar as configuracoes eh diretamente pela linha de codigo abaixo
    cenario = Cenario(20, 20, 0.1)

    while True:
        cenario.processar_eventos(pygame.event.get())
        cenario.contagem_tempo()
        pygame.display.update()


if __name__ == '__main__':
    main()
    # jogo_no_terminal()
