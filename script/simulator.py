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
    unit.Unit('u1@units-uk', 'localhost', 45101, {'lat': 51.650860, 'lng': -0.186010}),
    unit.Unit('u2@units-uk', 'localhost', 45102, {'lat': 51.651066, 'lng': -0.185838}),
    unit.Unit('u3@units-uk', 'localhost', 45103, {'lat': 51.651186, 'lng': -0.185613}),
    unit.Unit('u4@units-uk', 'localhost', 45104, {'lat': 51.651286, 'lng': -0.185441}),
    unit.Unit('u5@units-uk', 'localhost', 45105, {'lat': 51.651326, 'lng': -0.185291}),
    unit.Unit('u6@units-uk', 'localhost', 45106, {'lat': 51.651253, 'lng': -0.185162}),
    unit.Unit('u7@units-uk', 'localhost', 45107, {'lat': 51.651146, 'lng': -0.185076}),
    unit.Unit('u8@units-uk', 'localhost', 45108, {'lat': 51.651053, 'lng': -0.184969}),
    unit.Unit('u9@units-uk', 'localhost', 45109, {'lat': 51.650966, 'lng': -0.184872}),
    unit.Unit('u10@units-uk', 'localhost', 45110, {'lat': 51.650886, 'lng': -0.184818}),
]

DELAY = 15

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
                print('exc: Invalid word', l);

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
        # c = ''
        for n in names:
            # c += 'def {0} node={1} port={2}\n'.format(n.name, n.node, n.port)
            c = 'def {0} node={1} port={2}\n'.format(n.name, n.node, n.port)
            self._pipe.writePipe(c)
        # if c:
            # self._pipe.writePipe(c)
        while True:
            t = time.time()
            c = ''
            for n in names:
                # c += 'call fr ut02 {name}\n'.format(name=n.name)
                c = 'call fr ut02 {name}\n'.format(name=n.name)
            # if c:
                self._pipe.writePipe(c)
            time.sleep(DELAY - (time.time() - t))

    def __str__(self):
        pass


if __name__ == '__main__':
    Simulator('localhost', 45313, 'in', 'out')
