#! /usr/bin/env python3

#
# Created by Gustavo Viegas on 2017/06
#

import threading
import time
import connection
import message
import npipe

# TODO: move this
NAMES = [
    {'name': 'a', 'node': 'localhost', 'port': 10101},
    {'name': 'b', 'node': 'localhost', 'port': 10102},
    {'name': 'c', 'node': 'localhost', 'port': 10103}
]

class Simulator:
    """The Contic Simulator module"""
    def __init__(self, host, port, fifo_w, fifo_r):
        self._conn = None # connection.Connection(host, port)
        self._pipe = npipe.Npipe(fifo_w, fifo_r)
        self._th1 = threading.Thread(target=self._controller)
        self._th2 = threading.Thread(target=self._sender)
        self._start()

    def _start(self):
        self._th1.start()
        self._th2.start()
        self._receiver()

    def _receiver(self):
        while True:
            l = self._pipe.readPipe()
            print('got', l, end='', flush=True)
        """
        enqueue
        read pipe...
        """

    def _sender(self):
        """
        wait push on queue
        to JSON
        send to server
        wait push on queue...
        """
        pass

    def _controller(self, names=NAMES):
        c = ''
        for n in names:
            c += 'def {name} node={node} port={port}\n'.format(**n)
        if c:
            self._pipe.writePipe(c)
        self._pipe.writePipe('ls\n') # debug
        """
        set interval
        wait interval
        calls
        wait interval...
        """
    def __str__(self):
        pass


if __name__ == '__main__':
    Simulator('localhost', 45313, 'in', 'out')
