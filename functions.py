import classes  # importada apenas para definir o tipo de dado esperado pela funcao: escolha_posicao


def escolha_config():
    """responsavel por retornar as configuracoes (quantidade de linhas e colunas e dificulade) do novo jogo do usuario
    None -> tuple(int, int, float)"""
    lines = trata_escolha('quantidade de linhas')
    columns = trata_escolha('quantidade de colunas')
    difficulty = trata_escolha('dificuldade (0.1 à 0.9)', _int=False)
    return lines, columns, difficulty


def trata_escolha(mensagem: str, maximo: int | None = None, _int: bool = True):
    """responsavel pelo tratamento das entradas de dados do usuario antes, durante e apos a partida
    str, int | None, bool -> int | float"""
    while True:
        choice = input(f'Escolha a {mensagem}: ')
        if _int:  # caso _int seja True, a variavel choice só pode receber dados do tipo int
            try:
                choice = int(choice)          # verifica se a variavel choice realmente eh do tipo int
                if maximo is not None:        # se a variavel maximo for passada...
                    if 0 <= choice < maximo:  # ...significa que o jogador só pode escolher valores dentro de um intervalo
                        return choice
                    else:
                        erros(1, maximo)
                else:
                    return choice
            except ValueError:  # se subir a exceção do tipo ValueError quer dizer que nao eh do tipo int e chama a funcao de erros
                erros(2)
        else:  # caso contrario, a variavel choice só pode receber dados do tipo float
            try:
                choice = float(choice)      # verifica se a variavel choice realmente eh do tipo int
                if 0.1 <= choice <= 0.9:   # range de dificuldade mínima e máxima que o jogador pode escolher
                    return choice
                else:
                    erros(4)    # se a escolha de dificuldade estiver fora do range definido, chamar a funcao de erros
            except ValueError:  # se subir a exceção do tipo ValueError quer dizer que nao eh do tipo int e chama a funcao de erros
                erros(3)


def reinicio(mensagem: str):
    """chamada ao final de cada partida para perguntar se o jogador que iniciar um novo jogo ou sair do programa
    str -> bool"""
    print(f'\nVocê {mensagem}')

    while True:
        escolha = input('\nDeseja iniciar uma nova partida?\nSim [s]\nNão [n]\nR: ')

        if escolha.upper() == 'S':
            return True

        elif escolha.upper() == 'N':
            return False

        else:
            print('\nComando Inválido!\nDigite apenas "s" para Sim ou "n" para Não')


def escolha_posicao(lines: int, columns: int, campo: classes.CampoMinado):
    """funcao responsavel por retorna linha e coluna escolhida pelo usuario
    int, int, CampoMinado"""
    while True:
        line = trata_escolha('linha', maximo=lines)
        column = trata_escolha('coluna', maximo=columns)
        if posicao_livre(line, column, campo):
            return line, column


def posicao_livre(line: int, column: int, campo: classes.CampoMinado):
    """verifica se a posicao desejada do jogador esta livre para ser escolhida
    int, int, CampoMinado -> bool"""
    if campo.campo[line, column] == campo.elemento:
        return True
    else:
        erros(5, posicao=[line, column])


def erros(erro: int, maximo: int | None = None, posicao: list | None = None):
    """funcao responsavel por mostrar mensagens de erro ao jogador
    int, int | None, list -> None """
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
