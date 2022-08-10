from classes import CampoMinado
from functions import *


def main():
    jogo = True

    while jogo:
        lines, columns, difficulty = escolha_config()
        campo = CampoMinado(lines, columns, difficulty)
        campo.cria_bombas()
        campo.conta_bombas()
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


if __name__ == '__main__':
    main()
