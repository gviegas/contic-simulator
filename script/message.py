#! /usr/bin/env pyhton3

#
# Created by Gustavo Viegas on 2017/06
#

import json
import struct
from enum import Enum

EOM = '\n'

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
            return json.dumps(d)+EOM
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
                    p = s[1].split()
                    b = bytearray([int(x, 16) for x in p])
                    v = struct.unpack('f6B', b[:10])
                    d['data'] = {
                        'time': '20{0}-{1}-{2}-{3}-{4}-{5}'.format(*v[1:]),
                        'value': v[0]
                    }
            return json.dumps(d)+EOM
        else:
            print('Unknow type', type)

    @staticmethod
    def command(type, params=None):
        pass

    def __str__(self):
        pass
