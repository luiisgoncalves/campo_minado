from abc import ABC, abstractmethod

from Statistics import Statistics
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
        self._statistics = Statistics()

    def activate(self) -> bool | None:
        """responsavel por ativar o menu e tratar as opcoes escolhidas pelo jogador"""
        self._ative = True
        self.pause_time = time()
        while self._ative:
            choice = self.print_menus(1)
            match int(choice):
                case 1:
                    if self.campo is not None:  # so permite reinicio da partida se o campo do jogo tiver sido criado
                        return self.restart()
                    else:
                        self._erros(6)
                case 2:
                    self.statistics()
                case 3:
                    self._ative = False
                case 0:
                    self._ative = False
                    self._exit = True

            if not self._ative:
                self._log.beginning += time() - self.pause_time if self._log.beginning != 0 else 0  # subtrai o tempo que o jogo ficou pausado
                if self._exit:
                    self.exit()

    def save(self) -> None:
        """salva a partida no arquivo de log"""
        if self.campo is not None:  # novamente verifica e so permite no caso em que o campo minado tiver sido criado
            game = ''
            for i in range(len(self.campo.campo.flatten())):
                game += str(self.campo.campo.flatten()[i])
            print(game)
        else:
            self._erros(4)

    def restart(self) -> bool | None:
        """reinicia a partida"""
        while True:
            choice = input('deseja salvar o jogo atual?\n'
                           '[S] Sim\n'
                           '[N] Não\n'
                           'R: ')
            if choice.upper() == 'S':
                self.save()
            elif choice.upper() != 'N':
                self._erros(3)
                continue
            return True

    def statistics(self) -> None:
        """chamada quando o jogador deseja ver alguma estatistica do jogo"""
        while True:
            try:
                choice = self.print_menus(2)
                match choice:
                    case 1:
                        self._statistics.victory()
                    case 2:
                        self._statistics.loss()
                    case 3:
                        self._statistics.razao()
                    case 4:
                        self._statistics.time_sum()
                    case 0:
                        break
                    case _:
                        raise ValueError
            except FileNotFoundError:
                self._erros(2)

    def exit(self) -> None:
        """responsavel por encerrar a partida"""
        while True:
            try:
                choice = input('Certeza que deseja sair?\n'
                               '[S] Sim\n'
                               '[N] Não\n'
                               'R: ')
                if choice.upper() == 'S':
                    self._log.log[11] = 1
                    self._log.save()
                    exit()
                elif choice.upper() == 'N':
                    break
                else:
                    raise ValueError
            except ValueError:
                self._erros(5)

    def print_menus(self, type_menu: int) -> int:
        """mostra e pergunta ao usuario os menus e suas opcoes"""
        menu = []
        match type_menu:
            case 1:
                menu.append('|------- MENU -------|')
                menu.append('| [1] reiniciar      |')
                menu.append('| [2] estatisticas   |')
                menu.append('| [3] voltar ao jogo |')
                menu.append('| [0] sair           |')
                menu.append('|--------------------|')
            case 2:
                menu.append('|---------------- ESTATISTICAS ---------------|')
                menu.append('| [1] ranking de players que mais ganharam    |')
                menu.append('| [2] ranking de players que mais perderam    |')
                menu.append('| [3] porcentagem de vitorias de cada jogador |')
                menu.append('| [4] media de tempo de jogo                  |')
                menu.append('| [0] voltar                                  |')
                menu.append('|---------------------------------------------|')
        print()
        for opcao in menu:
            print(opcao)

        while True:
            try:
                choice = int(input('escolha sua opcao: '))
                if 0 <= choice <= len(menu) - 3:
                    return choice
                else:
                    raise ValueError
            except ValueError:
                self._erros(5)
                for opcao in menu:
                    print(opcao)

    @classmethod
    def _erros(cls, erro: int) -> None:
        """funcao responsavel por mostrar mensagens de erro ao jogador"""
        match erro:
            case 1:
                print('Comando inválido!')
            case 2:
                print('Arquivo de log não encontrado, verifique se o arquivo se encontra no mesmo diretorio do jogo.')
            case 3:
                print('\nEntrada Inválida!\n')
            case 4:
                print('\nImpossível salvar! Campo não criado\n')
            case 5:
                print('\nEntrada inválida! Entre apenas com o número da opção desejada!\n')
            case 6:
                print('\nReinício disponível apenas após criar uma partida!')


# menu do jogo rodado em GUI
class MenuGUI(Menu):
    def __init__(self, log: Log):
        super().__init__(log)

    def restart(self):
        pass

    def statistics(self):
        pass

    def exit(self):
        pass

    def activate(self):
        pass


if __name__ == '__main__':
    log_ = Log()
    MenuTerminal(log_).statistics()
