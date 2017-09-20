import lcm
import time
from exlcm import ax_control_t
from exlcm import eng_control_t

lc = lcm.LCM()

ax_msg = ax_control_t()
ax_msg.source = 'remote'


test_message = eng_control_t()
test_message.martin = False
test_message.start_ignite = True


while True:
	lc.publish("ax_control", ax_msg.encode())
	lc.publish("test", test_message.encode())

	print 'Printing..'
	time.sleep(2)
