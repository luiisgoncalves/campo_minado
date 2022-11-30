from abc import ABC, abstractmethod
import pandas as pd

from Log import Log
from time import time
from CampoMinado import CampoMinado


# classe abstrata de modelo para as classes dos menus especificos
class Menu(ABC):
    def __init__(self, log: Log):
        self._log = log

    @abstractmethod
    def activate(self):
        pass

    @abstractmethod
    def statistics(self):
        pass

    @abstractmethod
    def settings(self):
        pass

    @abstractmethod
    def restart(self):
        pass

    @abstractmethod
    def exit(self):
        pass


# menu do jogo rodado no terminal
class MenuTerminal(Menu):
    def __init__(self, log: Log, campo: CampoMinado | None = None):
        super().__init__(log)
        self._ative = False
        self._exit = False
        self.pause_time = 0
        self.campo = campo
        self.player = ''

    def activate(self):
        self._ative = True
        self.pause_time = time()
        while self._ative:
            print('\n|------- MENU -------|')
            self.print_opcoes(['| [1] salvar         |',
                               '| [2] carregar jogo  |',
                               '| [3] estatisticas   |',
                               '| [4] reiniciar      |',
                               '| [5] voltar ao jogo |',
                               '| [0] sair           |',
                               '|--------------------|'])
            choice = input('escolha sua opcao: ')
            try:
                match int(choice):
                    case 1:
                        self.save()
                    case 2:
                        pass
                    case 3:
                        pass
                    case 4:
                        if self.campo is not None:
                            return self.restart()

                        else:
                            self.erros(7)
                    case 5:
                        self._ative = False
                    case 0:
                        self._ative = False
                        self._exit = True
                    case _:
                        raise ValueError
            except ValueError:
                self.erros(6)

            if not self._ative:
                self._log.beginning += time() - self.pause_time if self._log.beginning != 0 else 0
                if self._exit:
                    self.exit()

    def save(self):
        if self.campo is not None:
            game = ''
            for i in range(len(self.campo.campo.flatten())):
                game += str(self.campo.campo.flatten()[i])
            print(game)
        else:
            self.erros(5)

    def restart(self):
        while True:
            choice = input('deseja salvar o jogo atual?\n'
                           '[S] Sim\n'
                           '[N] Não\n'
                           'R: ')
            if choice.upper() == 'S':
                self.save()
            elif choice.upper() != 'N':
                self.erros(4)
                continue
            return True

    @staticmethod
    def print_opcoes(opcoes):
        for opcao in opcoes:
            print(opcao)

    def statistics(self):
        try:
            df = pd.read_csv('log.csv', index_col=0)
            df.index = pd.to_datetime(df.index)
            print(df)
        except FileNotFoundError:
            self.erros(2)

    def settings(self):
        pass

    def exit(self):
        # self._log.log[15] = 1  # implementacao futura
        self._log.log[11] = 1
        self._log.save()
        exit()

    @classmethod
    def erros(cls, erro: int) -> None:
        """funcao responsavel por mostrar mensagens de erro ao jogador"""
        match erro:
            case 1:
                print(f'Comando inválido!')
            case 2:
                print('Arquivo de log não encontrado, verifique se o arquivo se encontra no mesmo diretorio do jogo.')
            case 3:
                print('Entrada Inválida!\nEntre apenas com um número do tipo float.')
            case 4:
                print('\nEntrada Inválida!\n')
            case 5:
                print('\nImpossível salvar! Campo não criado\n')
            case 6:
                print('\nEntrada inválida! Entre apenas com o número da opção desejada!')
            case 7:
                print('\nReinício disponível apenas após criar uma partida!')


# menu do jogo rodado em GUI
class MenuGUI(Menu):
    def __init__(self, log: Log):
        super().__init__(log)

    def restart(self):
        pass

    def statistics(self):
        pass

    def settings(self):
        pass

    def exit(self):
        pass

    def activate(self):
        pass


if __name__ == '__main__':
    log_ = Log()
    MenuTerminal(log_).statistics()
