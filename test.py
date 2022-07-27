from random import randint


class Campo:
    def __init__(self, linhas, colunas, elemento='·'):
        self.linhas = linhas
        self.colunas = colunas
        self.elemento = elemento

        self.campo = []
        for i in range(self.linhas):
            linha = []
            for j in range(self.colunas):
                linha.append(self.elemento)
            self.campo.append(linha)

    def mostra_campo(self, campo_minado=None, espacamento='   '):
        # print da numeracao das colunas
        for i in range(self.colunas):
            print(i, end=espacamento)
        print()

        # mostrar o campo minado
        for j in range(self.linhas):
            for k in range(self.colunas):
                if campo_minado is None:
                    print(self.campo[j][k], end=espacamento)
                else:
                    print(campo_minado[j][k], end=espacamento)

            # print da numeracao das linhas
            print(j)


class CampoMinado(Campo):
    def __init__(self, linhas, colunas, dificulade, elemento='·'):
        super().__init__(linhas, colunas, elemento)
        self.dificuldade = dificulade
        self.maximo = self.linhas * self.colunas
        self.campo_minado = self.copia_campo()

    def copia_campo(self):
        campo_minado = []
        for i in self.campo:
            linha = []
            for item in i:
                linha.append(item)
            campo_minado.append(linha)
        return campo_minado

    def cria_bombas(self):
        maximo = self.linhas * self.colunas
        bombas = []
        quantidade_bombas = int(self.dificuldade * maximo)
        i = 0
        while i < quantidade_bombas:
            posicao_bomba = randint(0, maximo-1)
            if posicao_bomba not in bombas:
                bombas.append(posicao_bomba)
                i += 1

        self.adiciona_bombas(bombas)

        ##################
        print(len(bombas))
        bombas.sort()
        print(bombas)
        ##################

    def adiciona_bombas(self, bombas, elemento='X'):
        for bomba in bombas:
            linha = bomba // self.linhas
            coluna = bomba % self.colunas
            self.campo_minado[linha][coluna] = elemento
