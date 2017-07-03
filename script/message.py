#! /usr/bin/env pyhton3

#
# Created by Gustavo Viegas on 2017/06
#

import json
from enum import Enum

class Requests(Enum):
    """Requests to server"""
    CREATE = 'create'
    UPDATE = 'update'

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

    @staticmethod
    def json(type, data, units=[]):
        if(type == Requests.CREATE):
            d = {'request': Requests.CREATE.value}
            d['id'] = data.name
            d['coords'] = data.coords
            return json.dumps(d)
        elif(type == Requests.UPDATE):
            d = {'request': Requests.UPDATE.value}
            for e in data:
                s = e.split(':')
                if s[0] == 'From':
                    for u in units:
                        if str(u) == s[1]:
                            d['id'] = u.name
                            break
                    else:
                        print('{} not mapped'.format(s[1]))
                        break
                elif s[0] == 'Data':
                    d['data'] = s[1]
            return json.dumps(d)
        else:
            print('Unknow type', type)

    @staticmethod
    def command(type, params=None):
        pass

    def __str__(self):
        pass
