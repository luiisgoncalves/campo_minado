from datetime import datetime
from time import time
import numpy as np


class Log:
    def __init__(self):
        self.file_name = 'log.csv'
        self.header = 'date,time,clicks,flags,correct_flags,fake_flags,doubt,player,win,lose,restart,quit,lines,columns,difficulty'
        self.log = np.zeros(self.header.count(',') + 1, dtype=object)
        self.log[0] = datetime.now()
        self.inicio = time()
        self.generate_header()

    def save(self, new=False):
        if new:
            with open(self.file_name, mode='w') as file:
                file.write(self.header + '\n')
        else:
            with open(self.file_name, mode='a+') as file:
                self.log[1] = round(time() - self.inicio, 5)
                content = ','.join([str(x) for x in self.log])
                file.write(content + '\n')

    def generate_header(self):
        try:
            with open(self.file_name):
                pass
        except FileNotFoundError:
            self.save(new=True)


if __name__ == '__main__':
    Log().save()
