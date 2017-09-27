import lcm
import RPi.GPIO as GPIO
import time

from exlcm import eng_status_t


#create tail lights object
tailLights = TailLights() # PINOUT HERE!!

def run():
    while True:
        lc.handle()
        tailLights()

class TailLights(GPIO):
    def __init__(self, leftPin=1, rightPin=2, brakePin=3, **kwargs):
        super(TailLights, self).__init__()
        self.leftPin = leftPin
        self.rightPin = rightPin
        self.brakePin = brakePin

        self.setmode(self.BCM)
        self.setup(self.leftPin, self.OUT)
        self.setup(self.rightPin, self.OUT)
        self.setup(self.brakePin, self.OUT)
        
        self.last = [False, False, False] #left signal and hazard

    def __call__(self):
        self.output(self.brakePin, brake)

        if leftSignal is False and rightSignal is False and hazards is False:
            self.output(self.leftPin, False)
            self.output(self.rightPin, False)

        elif hazards is True and hazards is not self.last[2]:
            self.output(self.leftPin, True)
            self.output(self.rightPin, True)
            self.last[2] = hazards

        elif leftSignal is True and leftSignal is not self.last[0]:
            self.output(self.leftPin, True)
            self.output(self.rightPin, False)
            self.last[0] = leftSignal

        elif rightSignal is True and rightSignal is not self.last[1]:
            self.output(self.leftPin, False)
            self.output(self.rightPin, True)
            self.last[1] = rightSignal

        else:
            if hazards is False:
            self.last[2] = False
        
            if leftSignal is False:
            self.last[0] = False

            if rightSignal is False:
            self.last[1] = False
        

#LCM Handlers
def lights_status_handler(channel, data):
    global leftSignal, rightSignal, hazards, brake
    msg = lights_control_t.decode(data)

    leftSignal = msg.leftSignal
    rightSignal = msg.rightSignal
    hazards = msg.hazards
    brake = msg.brake

# Init LCM
lc = lcm.LCM()
lights_status_sub = lc.subscribe("lights_status", lights_status_handler)


try:
    run()
except KeyboardInterrupt:
    pass
finally:    
    tailLights.cleanup()