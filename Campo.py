import numpy as np
from Log import Log


class Campo:
    def __init__(self, linhas: int, colunas: int, elemento: str = '·') -> None:
        """metodo de inicializacao da classe Campo.
        cria a quantidade de linhas, colunas os elementos neutros (ja com valor default) e o ndarray que representa a matriz do campo vazio"""
        self.linhas = linhas
        self.colunas = colunas
        self._elemento = elemento
        self.campo = np.full((self.linhas, self.colunas), self._elemento)
        self.log = Log()                 # LOG
        self.log.log[12] = self.linhas   # LOG
        self.log.log[13] = self.colunas  # LOG

    def mostra_campo(self, campo_minado: list | np.ndarray | None = None, espacamento: str = '   ') -> None:
        """metodo responsavel por mostrar o campo no estado atual"""
        # print da numeracao das colunas
        for i in range(self.colunas):
            print(str(i).ljust(len(espacamento) + 1), end='')

        print('\n' + '-- ' * (((self.colunas + self.colunas * len(espacamento)) // 3) + 1))

        # mostrar o campo minado
        for j in range(self.linhas):
            for k in range(self.colunas):
                if campo_minado is None:
                    print(self.campo[j][k], end=espacamento)
                else:
                    print(campo_minado[j][k], end=espacamento)

            # print da numeracao das linhas
            print('¦', j)

    @property
    def elemento(self) -> str:
        return self._elemento
