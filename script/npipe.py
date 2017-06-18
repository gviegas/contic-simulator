#! /usr/bin/env python3

#
# Created by Gustavo Viegas on 2017/06
#

from os import path, mkfifo
from threading import Thread

fifo_w = 'in'
fifo_r = 'out'

if not path.exists(fifo_w):
    mkfifo(fifo_w)
if not path.exists(fifo_r):
    mkfifo(fifo_r)

def readPipe():
    with open(fifo_r) as f:
        while True:
            l = f.readline()
            if not l:
                print('Pipe closed - done reading')
                break
            print(l, end='')

def writePipe():
    with open(fifo_w, 'w') as f:
        while True:
            f.write(input() + '\n')
            f.flush()

Thread(target=readPipe).start()
writePipe()
