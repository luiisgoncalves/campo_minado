def escolha_config():
    lines = trata_escolha('quantidade de linhas')
    columns = trata_escolha('quantidade de colunas')
    difficulty = trata_escolha('dificuldade (0.1 à 0.9)', _int=False)
    return lines, columns, difficulty


def trata_escolha(mensagem, maximo=None, _int=True):
    while True:
        choice = input(f'Escolha a {mensagem}: ')
        if _int:
            try:
                choice = int(choice)
                if maximo is not None:
                    if 0 <= choice < maximo:
                        return choice
                    else:
                        erros(1, maximo)
                else:
                    return choice
            except ValueError:
                erros(2)
        else:
            try:
                choice = float(choice)
                if 0.1 <= choice <= 0.9:
                    return choice
                else:
                    erros(4)
            except ValueError:
                erros(3)


def erros(erro, maximo=None, posicao=None):
    match erro:
        case 1:
            print(f'Fora do Range! Escolha um número entre 0 e {maximo - 1}')
        case 2:
            print('Entrada Inválida!\nEntre apenas com um número inteiro')
        case 3:
            print('Entrada Inválida!\nEntre apenas com um número do tipo float')
        case 4:
            print('Fora do Range! Escolha um número entre 0.1 e 0.9')
        case 5:
            print(f'A posição {posicao} já está ocupada, escolha outra')
        case 6:
            print(f'A posição {posicao} está com um aviso, deseja seleciona-la?')
