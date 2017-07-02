#! /usr/bin/env python3

#
# Created by Gustavo Viegas on 2017/06
#

from os import path, mkfifo
from threading import Thread

class Npipe:
    """Named pipe"""
    def __init__(self, fifo_w='in', fifo_r='out'):
        self._fifo_w = fifo_w
        self._fifo_r = fifo_r
        self._createPipes()

    @property
    def fifo_w(self):
        return self._fifo_w

    @property
    def fifo_r(self):
        return self._fifo_r

    def _createPipes(self):
        if not path.exists(self.fifo_w):
            mkfifo(self.fifo_w)
        if not path.exists(self.fifo_r):
            mkfifo(self.fifo_r)

    def readPipe(self):
        with open(self.fifo_r) as f:
            while True:
                l = f.readline()
                if not l:
                    print('Pipe closed - done reading')
                    break
                print(l, end='')

    def writePipe(self):
        with open(self.fifo_w, 'w') as f:
            while True:
                f.write(input() + '\n')
                f.flush()

    def __str__(self):
        return 'write end at "{0}"\nread end at "{1}"'\
            .format(self.fifo_w, self.fifo_r)

# pipe = Npipe()
# Thread(target=pipe.readPipe).start()
# pipe.writePipe()
