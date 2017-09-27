import sys
sys.path.append('../')

import lcm
import time
from exlcm import ax_control_t
from exlcm import eng_status_t
from exlcm import net_status_t
from exlcm import mode_control_t

lc = lcm.LCM()

test_message = eng_status_t()
test_message.running = True
test_message.rpm = 3500
test_message.speed = 43
test_message.temp = 321
test_message.fuel_flow = 346

signal_message = net_status_t()
signal_message.signal_str = 4

mode_message = mode_control_t()
mode_message.evos_mode = "DEV"

while True:
    lc.publish("eng_status", test_message.encode())
    lc.publish("net_status", signal_message.encode())
    lc.publish("mode_control", mode_message.encode())

    print 'Printing..'

    time.sleep(1)
