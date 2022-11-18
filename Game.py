from CampoMinado import CampoMinado


class Game:
    def __init__(self, terminal: bool = False):
        self.terminal = terminal
        self.lines = self.trata_escolha('quantidade de linhas')
        self.columns = self.trata_escolha('quantidade de colunas')
        self.difficulty = self.trata_escolha('dificuldade (0.1 à 0.9)', _int=False)
        self.campo = CampoMinado(self.lines, self.columns, self.difficulty)
        self.campo.mostra_campo()
        self.partida = True

    def game(self):
        while self.partida:
            line, column = self.escolha_posicao(self.lines, self.columns, self.campo)
            explosao = self.campo.escolha(line, column)
            self.campo.mostra_campo()

            if explosao:
                # self.partida = False
                # return self.reinicio('perdeu! :(')
                return self.reinicio('perdeu! :(')

            elif self.campo.qtd_posicoes_disponiveis() == self.campo.qtd_bombas:
                # self.partida = False
                return self.reinicio('ganhou!!!')

    @classmethod
    def escolha_posicao(cls, lines: int, columns: int, campo: CampoMinado) -> tuple[int, int]:
        """funcao responsavel por retorna linha e coluna escolhida pelo usuario"""
        while True:
            line = cls.trata_escolha('linha', maximo=lines)
            column = cls.trata_escolha('coluna', maximo=columns)
            if cls.posicao_livre(line, column, campo):
                return line, column

    @classmethod
    def posicao_livre(cls, line: int, column: int, campo: CampoMinado) -> bool | None:
        """verifica se a posicao desejada do jogador esta livre para ser escolhida"""
        if campo.campo[line, column] == campo.elemento:
            return True
        else:
            cls.erros(5, posicao=[line, column])

    @classmethod
    def reinicio(cls, mensagem: str) -> bool | None:
        """chamada ao final de cada partida para perguntar se o jogador que iniciar um novo jogo ou sair do programa"""
        print(f'\nVocê {mensagem}')

        while True:
            escolha = input('\nDeseja iniciar uma nova partida?\nSim [s]\nNão [n]\nR: ')

            if escolha.upper() == 'S':
                return True

            elif escolha.upper() == 'N':
                return False

            else:
                print('\nComando Inválido!\nDigite apenas "s" para Sim ou "n" para Não')

    @classmethod
    def trata_escolha(cls, mensagem: str, maximo: int | None = None, _int: bool = True) -> int | float:
        """responsavel pelo tratamento das entradas de dados do usuario antes, durante e apos a partida"""
        while True:
            choice = input(f'Escolha a {mensagem}: ')
            if _int:  # caso _int seja True, a variavel choice só pode receber dados do tipo int
                try:
                    choice = int(choice)  # verifica se a variavel choice realmente eh do tipo int
                    if maximo is not None:  # se a variavel maximo for passada...
                        if 0 <= choice < maximo:  # ...significa que o jogador só pode escolher valores dentro de um intervalo
                            return choice
                        else:
                            cls.erros(1, maximo)
                    else:
                        return choice
                except ValueError:  # se subir a exceção do tipo ValueError quer dizer que nao eh do tipo int e chama a funcao de erros
                    cls.erros(2)
            else:  # caso contrario, a variavel choice só pode receber dados do tipo float
                try:
                    choice = float(choice)  # verifica se a variavel choice realmente eh do tipo int
                    if 0.1 <= choice <= 0.9:  # range de dificuldade mínima e máxima que o jogador pode escolher
                        return choice
                    else:
                        cls.erros(4)  # se a escolha de dificuldade estiver fora do range definido, chamar a funcao de erros
                except ValueError:  # se subir a exceção do tipo ValueError quer dizer que nao eh do tipo int e chama a funcao de erros
                    cls.erros(3)

    @classmethod
    def erros(cls, erro: int, maximo: int | None = None, posicao: list | None = None) -> None:
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
                print(f'\nA posição [{posicao[0]},{posicao[1]}] não pode ser selecionada, escolha outra.\n')
            case 6:
                print(f'A posição {posicao} está com um aviso, deseja seleciona-la?')
