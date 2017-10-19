import sys
sys.path.append('../')

import lcm
from exlcm import ax_control_t
from exlcm import eng_control_t


def ax_handler(channel, data):
    msg = ax_control_t.decode(data)
    print msg.source


def eng_handler(channel, data):
    msg = eng_control_t.decode(data)
    print msg.martin


lc = lcm.LCM()
subscription = lc.subscribe("test", eng_handler)

try:
    while True:
        print 'Receiving..'
        lc.handle()
except KeyboardInterrupt:
    pass
