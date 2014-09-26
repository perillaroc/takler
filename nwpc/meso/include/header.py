#!/bin/env python

node_path = "$node_path$"

#################
# head
################

import atexit
import signal
import os
import sys
from datetime import datetime
import takler

print datetime.now()

sys.path.append(os.path.join(os.path.dirname(__file__), '../../include'))
import configure


client = takler.Client()


def init():
    client.init(node_path, str(os.getpid()))


def complete():
    client.complete(node_path)


def abort():
    client.abort(node_path)


def signal_handler(signum, frame):
    print "caught signal " + str(signum)
    abort()
    sys.exit(0)

signal.signal(signal.SIGINT,  signal_handler)
signal.signal(signal.SIGHUP,  signal_handler)
signal.signal(signal.SIGQUIT, signal_handler)
signal.signal(signal.SIGILL,  signal_handler)
signal.signal(signal.SIGTRAP, signal_handler)
signal.signal(signal.SIGIOT,  signal_handler)
signal.signal(signal.SIGBUS,  signal_handler)
signal.signal(signal.SIGFPE,  signal_handler)
signal.signal(signal.SIGUSR1, signal_handler)
signal.signal(signal.SIGUSR2, signal_handler)
signal.signal(signal.SIGPIPE, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGXCPU, signal_handler)
signal.signal(signal.SIGPWR,  signal_handler)

init()