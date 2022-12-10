from datetime import datetime
from time import time
import numpy as np


class Log:
    def __init__(self):
        self.file_name = 'log.csv'
        self.header = 'date,'           \
                      'time,'           \
                      'clicks,'         \
                      'flags,'          \
                      'correct_flags,'  \
                      'incorrect_flags,'\
                      'doubt,'          \
                      'player,'         \
                      'win,'            \
                      'lose,'           \
                      'restart,'        \
                      'quit,'           \
                      'lines,'          \
                      'columns,'        \
                      'difficulty,'     \
                      'GUI'
        self.log = np.zeros(self.header.count(',') + 1, dtype=object)
        self.log[0] = datetime.now()
        self.generate_header()
        self.beginning = 0

    def start(self) -> None:
        """marca o horario que o jogo iniciou"""
        self.beginning = time()

    def save(self, new=False) -> None:
        """salva a partida atual no arquivo de log ja existente ou cria um novo"""
        if new:
            with open(self.file_name, mode='w') as file:
                file.write(self.header + '\n')
        else:
            if self.beginning:
                with open(self.file_name, mode='a+') as file:
                    self.log[1] = round(time() - self.beginning, 5)
                    content = ','.join([str(x) for x in self.log])
                    file.write(content + '\n')

    def generate_header(self):
        """cria o cabecalho do arquivo de log"""
        try:
            with open(self.file_name):
                pass
        except FileNotFoundError:
            self.save(new=True)


if __name__ == '__main__':
    Log().save()
