import pygame
from functions import *
from Cenario import Cenario


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

            elif campo.qtd_posicoes_disponiveis() == campo.qtd_bombas:
                partida = False
                jogo = reinicio('ganhou!!!')


def main():
    # enquanto nao crio um menu, unico modo de alterar as configuracoes eh diretamente pela linha de codigo abaixo
    cenario = Cenario(10, 10, 0.05)

    while True:
        cenario.processar_eventos(pygame.event.get())
        cenario.contagem_tempo()
        pygame.display.update()


if __name__ == '__main__':
    main()
    # jogo_no_terminal()
