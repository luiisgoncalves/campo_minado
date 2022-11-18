import pandas as pd
# from tkinter import *


class Menu:
    def __init__(self):
        self.ativo = False
        self.player = ''

    @staticmethod
    def statistics():
        try:
            df = pd.read_csv('log.csv', index_col=0)
            df.index = pd.to_datetime(df.index)
            print(df)
        except FileNotFoundError:
            print('Arquivo de log nao encontrado, verifique se o mesmo se encontra no mesmo diretorio do jogo')

    def settings(self):
        pass


if __name__ == '__main__':
    Menu().statistics()
