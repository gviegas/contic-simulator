#! /usr/bin/env python3

#
# Created by Gustavo Viegas on 2017/06
#

import threading
import time
import json
import connection
import message
import npipe
import unit

# TODO: move this
UNITS = [
    unit.Unit('a', 'localhost', 35412, {'lat': 1, 'lng': 2})
]

DELAY = 5

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

    def _receiver(self):
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
                j = message.Message.json(message.Requests.UPDATE, d, UNITS)
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
                print('exc: Invalid word');

    def _sender(self, units=UNITS):
        for u in units:
            j = message.Message.json(message.Requests.CREATE, u)
            self._conn.send(j.encode())
        while True:
            if self._queue:
                e = self._queue.pop(0)
                b = e.encode()
                self._conn.send(b)
            else:
                time.sleep(3)

    def _controller(self, names=UNITS):
        c = ''
        for n in names:
            c += 'def {0} node={1} port={2}\n'.format(n.name, n.node, n.port)
        if c:
            self._pipe.writePipe(c)
        while True:
            t = time.time()
            c = ''
            for n in names:
                c += 'call fr ut02 {name}\n'.format(name=n.name)
            if c:
                self._pipe.writePipe(c)
            time.sleep(DELAY - (time.time() - t))

    def __str__(self):
        pass


if __name__ == '__main__':
    Simulator('localhost', 45313, 'in', 'out')
