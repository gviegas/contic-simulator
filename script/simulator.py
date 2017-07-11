#! /usr/bin/env python3

#
# Created by Gustavo Viegas on 2017/06
#

import threading
import time
import json
import connection
import npipe
from message import Message, Requests, Commands
from constants import DELAY, UNITS

class Simulator:
    """The Contic Simulator module"""
    def __init__(self, host, port, fifo_w, fifo_r):
        self._conn = connection.Connection(host, port)
        self._pipe = npipe.Npipe(fifo_w, fifo_r)
        self._queue = []
        self._th1 = threading.Thread(target=self._controller)
        self._th2 = threading.Thread(target=self._sender)
        self._start()

    def _start(self):
        self._th1.start()
        self._th2.start()
        self._receiver()

    def _receiver(self, units=UNITS):
        while True:
            l = self._pipe.readPipe().strip()
            if not l:
                time.sleep(3)
                continue
            elif l == '[OK]':
                d = []
                l = self._pipe.readPipe().strip()
                while l != '[EOF]':
                    d.append(l)
                    l = self._pipe.readPipe().strip()
                j = Message.json(Requests.UPDATE, d, units)
                self._queue.append(j)
            elif l == '[ERR]':
                d = {}
                l = self._pipe.readPipe().strip()
                while l != '[EOF]':
                    e = l.split(':')
                    d[e[0]] = e[1]
                    l = self._pipe.readPipe().strip()
                print('error:', d)
            else:
                print('exc: Invalid word', l);

    def _sender(self, units=UNITS):
        for u in units:
            j = Message.json(Requests.CREATE, u)
            self._conn.send(j.encode())
        while True:
            if self._queue:
                e = self._queue.pop(0)
                b = e.encode()
                self._conn.send(b)
            else:
                time.sleep(3)

    def _controller(self, units=UNITS):
        if not UNITS:
            return
        c = ''
        for u in units:
            c += Message.command(Commands.DEF, u)
        self._pipe.writePipe(c)
        while True:
            t = time.time()
            c = ''
            for u in units:
                c += Message.command(Commands.CALL, u, ['fr', 'ut02'])
            self._pipe.writePipe(c)
            time.sleep(DELAY - (time.time() - t))

    def __str__(self):
        pass


if __name__ == '__main__':
    Simulator('localhost', 43313, 'in', 'out')
