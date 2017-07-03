#! /usr/bin/env python3

#
# Created by Gustavo Viegas on 2017/06
#

class Unit:
    """Unit object"""
    def __init__(self, name, node, port, coords, data=[]):
        self._name = name
        self._node = node
        self._port = port
        self._coords = coords
        self._data = data

    @property
    def name(self):
        return self._name

    @property
    def node(self):
        return self._node

    @property
    def port(self):
        return self._port

    @property
    def coords(self):
        return self._coords

    @property
    def data(self):
        return self._data

    def __eq__(self, other):
        return self.node == other.node and self.port == other.port

    def __hash__(self):
        return hash(self.__str__())

    def __str__(self):
        return '{0} {1}'.format(self.node, self.port)
