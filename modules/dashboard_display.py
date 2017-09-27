import sys
sys.path.append('../')

import lcm
from exlcm import eng_status_t
from exlcm import net_status_t
from exlcm import mode_control_t

from kivy.config import Config

Config.set('graphics', 'borderless', 0)
Config.set('graphics', 'height', 480)
Config.set('graphics', 'width', 800)

from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

from kivy.clock import Clock


from kivy.core.window import Window
Window.clearcolor = (0.1, 0.1, 0.1, 1)


# Global vars
update_freq = 0.1
lap_counter = 1
num_laps = 10

# net_status
net_signal = 0

# mode_control
evos_mode = 'DEV'

# eng_status
eng_running = False
eng_fuel_flow = 0
eng_temp = 0
eng_rpm = 0

veh_speed = 0


# LCM handlers
def eng_status_handler(channel, data):
    global eng_running, eng_fuel_flow, eng_temp, eng_rpm, veh_speed
    msg = eng_status_t.decode(data)

    eng_running = msg.running
    eng_temp = msg.temp
    eng_rpm = msg.rpm
    veh_speed = msg.speed
    eng_fuel_flow = msg.fuel_flow


def net_status_handler(channel, data):
    global net_signal
    msg = net_status_t.decode(data)

    net_signal = msg.signal_str


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
    global evos_mode, update_freq

    def __init__(self, **kwargs):
        super(VehicleModeWidget, self).__init__(**kwargs)
        self.mode = evos_mode
        self.color = self.parse_color(evos_mode)
        Clock.schedule_interval(self.update, update_freq)

    def update(self, *args):
        self.ids.mode.text = evos_mode
        self.ids.mode.color = self.parse_color(evos_mode)

    def parse_color(self, current_mode):
        if current_mode == 'DEV':
            color = (0.3, 0.3, 0.3, 1)
        elif current_mode == 'SHOWROOM':
            color = (0.1, 0.1, 1, 1)
        else:
            color = (1, 0, 0, 1)

        return color

    pass


class LapWidget(BoxLayout):
    global lap_counter, num_laps, update_freq

    current_lap = StringProperty(str(lap_counter))
    max_lap = StringProperty(str(num_laps))
    pass


class IgnitionWidget(BoxLayout):
    global eng_running, update_freq

    running = StringProperty('DEFAULT')

    def __init__(self, **kwargs):
        super(IgnitionWidget, self).__init__(**kwargs)
        if eng_running:
            self.running = 'ON'
            self.color = (1, 0.1, 0.1, 1)
        else:
            self.running = 'OFF'
            self.color = (0.3, 0.3, 0.3, 1)
        Clock.schedule_interval(self.update, update_freq)

    def update(self, *args):
        if eng_running:
            self.ids.ignition.text = 'ON'
            self.ids.ignition.color = (1, 0.1, 0.1, 1)
        else:
            self.ids.ignition.text = 'OFF'
            self.ids.ignition.color = (0.3, 0.3, 0.3, 1)


class RPMWidget(BoxLayout):
    global update_freq, eng_rpm

    rpm = StringProperty('DEFAULT')

    def __init__(self, **kwargs):
        super(RPMWidget, self).__init__(**kwargs)

        self.rpm = str(eng_rpm)
        Clock.schedule_interval(self.update, update_freq)

    def update(self, *args):
        self.ids.RPM.text = str(eng_rpm)


class CopilotWidget(BoxLayout):
    pass


class SpeedWidget(BoxLayout):
    global update_freq, veh_speed

    speed = StringProperty('DEFAULT')

    def __init__(self, **kwargs):
        super(SpeedWidget, self).__init__(**kwargs)

        self.speed = str(veh_speed)
        Clock.schedule_interval(self.update, update_freq)

    def update(self, *args):
        self.ids.speed.text = str(veh_speed)


class SignalStrengthWidget(BoxLayout):
    global update_freq, net_signal

    signal = StringProperty(str(net_signal))

    def __init__(self, **kwargs):
        super(SignalStrengthWidget, self).__init__(**kwargs)

        self.signal = str(net_signal)
        Clock.schedule_interval(self.update, update_freq)

    def update(self, *args):
        self.ids.signal.text = str(net_signal)


class EngineTempWidget(BoxLayout):
    global update_freq, eng_temp

    temp = StringProperty(str(eng_temp))

    def __init__(self, **kwargs):
        super(EngineTempWidget, self).__init__(**kwargs)

        self.temp = str(eng_temp)
        Clock.schedule_interval(self.update, update_freq)

    def update(self, *args):
        self.ids.temp.text = str(eng_temp)


class FuelConsumptionWidget(BoxLayout):
    global update_freq, eng_fuel_flow

    fuel_flow = StringProperty(str(eng_fuel_flow))

    def __init__(self, **kwargs):
        super(FuelConsumptionWidget, self).__init__(**kwargs)

        self.fuel = str(eng_temp)
        Clock.schedule_interval(self.update, update_freq)

    def update(self, *args):
        self.ids.fuel.text = str(eng_fuel_flow)


class Rows(BoxLayout):
    pass


# Secret Widgets
class ExitWidget(BoxLayout):
    pass


# Creating App
class EVOSDashboardApp(App):

    # Kivy Variables
    ailerons_font = '../resources/fonts/ailerons/Ailerons-Typeface.otf'
    up_arrow = '../resources/images/up_arrow.png'

    def update_lcm(self, *args):
        lc.handle()

    def build(self):
        event = Clock.schedule_interval(self.update_lcm, 1/30.)
        rows = Rows()
        return rows


def run():
    EVOSDashboardApp().run()

run()
