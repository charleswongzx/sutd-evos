import sys
sys.path.append('../')

import lcm
import time
from exlcm import ax_control_t
from exlcm import veh_status_t
from exlcm import net_status_t
from exlcm import mode_control_t
from exlcm import eng_toggle_t

lc = lcm.LCM()

test_message = veh_status_t()
test_message.running = True
test_message.rpm = 3110
test_message.speed = 40
test_message.temp = 220
test_message.fuel_flow = 346
test_message.pressure = 1230

eng_toggle_msg = eng_toggle_t()
eng_toggle_msg.toggle = True


signal_message = net_status_t()
signal_message.signal_str = 4

mode_message = mode_control_t()
mode_message.evos_mode = "DEV"

while True:


    lc.publish("eng_status", test_message.encode())
    lc.publish("net_status", signal_message.encode())
    lc.publish("mode_control", mode_message.encode())
    lc.publish("eng_toggle", eng_toggle_msg.encode())

    print 'Printing..'

    time.sleep(1)
    test_message.rpm += 1
    eng_toggle_msg.toggle = ~eng_toggle_msg.toggle
