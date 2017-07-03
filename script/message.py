#! /usr/bin/env pyhton3

#
# Created by Gustavo Viegas on 2017/06
#

from enum import Enum

class Commands(Enum):
    """Available commands"""
    LS = 'ls'
    DEF = 'def'
    UNDEF = 'undef'
    CALL = 'call'

class Message:
    """Message creation & manipulation"""
    def __init__(self):
        pass

    def toJson(self, data):
        pass

    def toCommand(self, data):
        pass

    def json(self, data):
        pass

    def command(self, type, params=None):
        pass

    def __str__(self):
        pass
