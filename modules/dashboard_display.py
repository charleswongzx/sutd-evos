import sys
sys.path.append('../')

import lcm
from exlcm import eng_status_t
from exlcm import net_status_t
from exlcm import mode_control_t

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout

from kivy.vector import Vector
from kivy.clock import Clock


# Global vars
lap_counter = 0

# net_status
signal_str = 0

# mode_control
evos_mode = 0

# eng_status
fuel_flow = 0
running = 0
speed = 0
temp = 0
rpm = 0


# LCM handlers
def eng_status_handler(channel, data):
    global running, temp, rpm, speed, fuel_flow
    msg = eng_status_t.decode(data)

    running = msg.running
    temp = msg.temp
    rpm = msg.rpm
    speed = msg.speed
    fuel_flow = msg.fuel_flow


def net_status_handler(channel, data):
    global signal_str
    msg = net_status_t.decode(data)

    signal_str = msg.signal_str


def mode_control_handler(channel, data):
    global evos_mode
    msg = mode_control_t.decode(data)

    evos_mode = msg.evos_mode


# Init LCM
lc = lcm.LCM()
eng_status_sub = lc.subscribe("eng_status", eng_status_handler)
net_status_sub = lc.subscribe("net_status", net_status_handler)
mode_control_sub = lc.subscribe("mode_control", mode_control_handler)


class VehicleModeWidget(Widget):
    pass


class LapWidget(Widget):
    pass


class IgnitionWidget(Widget):
    pass


class RPMWidget(Widget):
    pass


class CopilotWidget(Widget):
    pass


class SpeedWidget(Widget):
    pass


class SignalStrengthWidget(Widget):
    pass


class EngineTempWidget(Widget):
    pass


class FuelConsumptionWidget(Widget):
    pass


class DashboardApp(App):
    title = 'evos_dashboard'
    # lc.handle()

    def build(self):
        rows = BoxLayout(orientation='vertical')

        return Button(text='HELLO',
                      font_size=150)


def run():
    DashboardApp().run()


run()
