#! /usr/bin/env pyhton3

#
# Created by Gustavo Viegas on 2017/06
#

import socket

class Connection:
    """TCP connection with a server"""
    def __init__(self, host, port):
        self._at = (host, port)
        self._socket = None
        if not self._connect():
            raise OSError('Could not connect to {} {}'.format(host, port))

    @property
    def at(self):
        return self._at

    def _connect(self):
        info = socket.getaddrinfo(self.at.value[0], self.at.value[1],
            socket.AF_UNSPEC, socket.SOCK_STREAM)
        for r in info:
            family, stype, proto, cname, addr = r
            try:
                self._socket = socket.socket(family, stype, proto)
            except OSError as ex:
                self._socket = None
                continue
            try:
                self._socket.connect(addr)
            except OSError as ex:
                self._socket.close()
                self._socket = None
                continue
            return True
        return False

    def send(self, msg):
        if self._socket:
            try:
                s = self._socket.sendall(msg)
            except OSError as ex:
                # TODO
                return s

    def recv(self):
        if self._socket:
            return self.socket.recv(4096)

    def __str__(self):
        pass
