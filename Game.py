from CampoMinado import CampoMinado
from Menus import MenuTerminal, MenuGUI
from Log import Log


class Game:
    def __init__(self, terminal: bool = True):
        self.log = Log()
        self.terminal = terminal
        self.menu = MenuTerminal(self.log) if terminal else MenuGUI(self.log)
        self.log.log[7] = input('Quem irá jogar: ').upper()
        self.lines = self.trata_escolha('quantidade de linhas')
        self.columns = self.trata_escolha('quantidade de colunas')
        self.difficulty = self.trata_escolha('dificuldade (0.1 à 0.9)', _int=False)
        self.campo = CampoMinado(self.lines, self.columns, self.difficulty, self.log)
        self.campo.mostra_campo()
        self.partida = True
        self.menu.campo = self.campo
        self.log.start()

    def game(self):
        """doc"""
        while self.partida:
            try:
                line, column = self.escolha_posicao()
                explosao = self.campo.escolha(line, column)
                self.campo.mostra_campo()

                if explosao:
                    self.campo.log.log[9] = 1
                    self.save()
                    return self.reinicio('perdeu! :(')

                elif self.campo.qtd_posicoes_disponiveis() == self.campo.qtd_bombas:
                    self.campo.log.log[8] = 1
                    self.save()
                    return self.reinicio('ganhou!!!')
            except TypeError:
                break

    def player(self):
        """doc"""
        self.log.log[7] = input('Quem está jogando?\nR: ')

    def save(self):
        """doc"""
        self.campo.log.save()

    def escolha_posicao(self) -> tuple[int, int]:
        """funcao responsavel por retorna linha e coluna escolhida pelo usuario"""
        while True:
            line = self.trata_escolha('linha', line=True)
            if line is None:
                break

            column = self.trata_escolha('coluna', column=True)
            if column is None:
                break

            if self.posicao_livre(line, column):
                return line, column

    def posicao_livre(self, line: int, column: int) -> bool | None:
        """verifica se a posicao desejada do jogador esta livre para ser escolhida"""
        if self.campo.campo[line, column] == self.campo.elemento:
            return True
        else:
            self._erros(5, posicao=[line, column])

    @classmethod
    def reinicio(cls, mensagem: str) -> bool | None:
        """chamada ao final de cada partida para perguntar se o jogador que iniciar um novo jogo ou sair do programa"""
        print(f'\nVocê {mensagem}')

        while True:
            escolha = input('\nDeseja iniciar uma nova partida?\n[S] Sim\n[N] Não\nR: ')

            if escolha.upper() == 'S':
                return True

            elif escolha.upper() == 'N':
                return False

            else:
                print('\nComando Inválido!\nDigite apenas "s" para Sim ou "n" para Não')

    def trata_escolha(self, mensagem: str, line: bool = False, column: bool = False, _int: bool = True) -> int | float:
        """responsavel pelo tratamento das entradas de dados do usuario antes, durante e apos a partida"""
        while True:
            choice = input(f'Escolha a {mensagem}: ')
            if choice.upper() == 'PAUSE':
                if self.pause():
                    try:
                        self.campo.mostra_campo()
                    except AttributeError:
                        pass
                else:
                    break
                continue

            if _int:  # caso _int seja True, a variavel choice só pode receber dados do tipo int
                try:
                    choice = int(choice)  # verifica se a variavel choice realmente eh do tipo int

                    if line:
                        if 0 <= choice < self.lines:  # ...significa que o jogador só pode escolher valores dentro de um intervalo
                            return choice
                        else:
                            self._erros(1, self.lines)

                    elif column:
                        if 0 <= choice < self.columns:  # ...significa que o jogador só pode escolher valores dentro de um intervalo
                            return choice
                        else:
                            self._erros(1, self.columns)

                    else:
                        return choice

                except ValueError:  # se subir a exceção do tipo ValueError quer dizer que nao eh do tipo int e chama a funcao de erros
                    self._erros(2)
            else:  # caso contrario, a variavel choice só pode receber dados do tipo float
                try:
                    choice = float(choice)  # verifica se a variavel choice realmente eh do tipo int
                    if 0.1 <= choice <= 0.9:  # range de dificuldade mínima e máxima que o jogador pode escolher
                        return choice
                    else:
                        self._erros(4)  # se a escolha de dificuldade estiver fora do range definido, chamar a funcao de erros
                except ValueError:  # se subir a exceção do tipo ValueError quer dizer que nao eh do tipo int e chama a funcao de erros
                    self._erros(3)

    def pause(self):
        """doc"""
        if self.menu.activate():
            self.log.log[10] = 1
            self.log.save()
            return False

        return True

    @classmethod
    def _erros(cls, erro: int, maximo: int | None = None, posicao: list | None = None) -> None:
        """funcao responsavel por mostrar mensagens de erro ao jogador"""
        match erro:
            case 1:
                print(f'Fora do Range! Escolha um número entre 0 e {maximo - 1}.')
            case 2:
                print('Entrada Inválida!\nEntre apenas com um número inteiro.')
            case 3:
                print('Entrada Inválida!\nEntre apenas com um número do tipo float.')
            case 4:
                print('Fora do Range! Escolha um número entre 0.1 e 0.9')
            case 5:
                print(f'\nA posição ({posicao[0]},{posicao[1]}) não pode ser selecionada, escolha outra.\n')
            case 6:
                print(f'A posição {posicao} está com um aviso, deseja seleciona-la?')
