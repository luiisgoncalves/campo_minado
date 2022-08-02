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
            line = trata_escolha('linha', lines)
            column = trata_escolha('coluna', columns)
            explosao = campo.escolha(line, column)
            campo.mostra_campo()

            if explosao:
                partida = False
                print('Você perdeu!!')
                escolha = input('Deseja iniciar uma nova partida?\nSim [s]\nNão [n]\nR: ')

                if escolha.upper() == 'N':
                    jogo = False


if __name__ == '__main__':
    main()
