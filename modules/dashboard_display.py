import sys
sys.path.append('../')

import lcm
from exlcm import eng_status_t
from exlcm import net_status_t
from exlcm import mode_control_t

from kivy.config import Config

Config.set('graphics', 'borderless', 1)
Config.set('graphics', 'height', 480)
Config.set('graphics', 'width', 800)

from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty
from kivy.properties import BooleanProperty
from kivy.properties import StringProperty


from kivy.core.window import Window
Window.clearcolor = (0.1, 0.1, 0.1, 1)


# Global vars
lap_counter = 1
num_laps = 10

# net_status
net_signal = 0

# mode_control
evos_mode = 0

# eng_status
eng_running = 0
eng_fuel_flow = 0
eng_temp = 0
eng_rpm = 0

veh_speed = 0

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


# Creating widgets
class VehicleModeWidget(BoxLayout):
    if evos_mode == 0:
        mode = StringProperty('DEV')
        color = (0.3, 0.3, 0.3, 1)
    elif evos_mode == 1:
        mode = StringProperty('SHOWROOM')
        color = (0.1, 0.1, 1, 1)
    elif evos_mode == 2:
        mode = StringProperty('RACE')
        color = (1, 0, 0, 1)

    pass


class LapWidget(BoxLayout):
    current_lap = StringProperty(str(lap_counter))
    max_lap = StringProperty(str(num_laps))
    pass


class IgnitionWidget(BoxLayout):
    if eng_running:
        running = StringProperty('RUNNING')
        color = (1, 0.1, 0.1, 1)
    else:
        running = StringProperty('OFF')
        color = (0.3, 0.3, 0.3, 1)
    pass


class RPMWidget(BoxLayout):
    rpm = StringProperty(str(eng_rpm))
    pass


class CopilotWidget(BoxLayout):
    pass


class SpeedWidget(BoxLayout):
    speed = StringProperty(str(veh_speed))
    pass


class SignalStrengthWidget(BoxLayout):
    signal = StringProperty(str(net_signal))
    pass


class EngineTempWidget(BoxLayout):
    temp = StringProperty(str(eng_temp))
    pass


class FuelConsumptionWidget(BoxLayout):
    fuel_flow = StringProperty(str(eng_fuel_flow))
    pass


class Rows(BoxLayout):
    pass


# Secret Widgets
class ExitWidget(BoxLayout):
    pass


# Creating App
class EVOSDashboardApp(App):
    # lc.handle()

    # Kivy Variables
    ailerons_font = '../resources/fonts/ailerons/Ailerons-Typeface.otf'
    up_arrow = '../resources/images/up_arrow.png'

    def build(self):
        return Rows()


def run():
    EVOSDashboardApp().run()


run()
