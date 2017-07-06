#! /usr/bin/env python3

#
# Created by Gustavo Viegas on 2017/06
#

import time
from os import path, mkfifo
from threading import Thread

class Npipe:
    """Named pipe"""
    def __init__(self, fifo_w='in', fifo_r='out'):
        self._fifo_w = fifo_w
        self._fifo_r = fifo_r
        self._fw = None
        self._fr = None
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
        if not self._fr:
            self._fr = open(self.fifo_r, buffering=1)
        return self._fr.readline()

    def writePipe(self, data):
        if not self._fw:
            self._fw = open(self.fifo_w, 'w', buffering=1)
        self._fw.write(data)

    def __str__(self):
        return 'write end at "{0}"\nread end at "{1}"'\
            .format(self.fifo_w, self.fifo_r)
