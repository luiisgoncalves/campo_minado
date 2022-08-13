from classes import CampoMinado, Cenario
import pygame
from functions import *


def main():
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


def teste():

    cenario = Cenario(15, 15, 0.05)
    jogo = True
    while jogo:
        partida = True

        while partida:
            cenario.processar_eventos(pygame.event.get())
            pygame.display.update()
            cenario.pinta_qntd_bomba()
            cenario.contagem_tempo()
            perdeu = cenario.perdeu()
            venceu = cenario.venceu()

            if venceu or perdeu:
                partida = False


if __name__ == '__main__':
    # main()
    teste()
