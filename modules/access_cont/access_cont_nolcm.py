import serial
import time
import RPi.GPIO as GPIO

time_stamp=time.time()
time_now=time.time()
time_speed=time.time()



def run():
    global time_speed
    time_stamp=time.time()
    ard=serial.Serial('/dev/ttyACM0',115200)
    GPIO.setmode(GPIO.BCM)
    lightbuttonpins = [4,5,6,7,8,9]
    relaybuttonpins_r=[16,17,18,19] #to relay
    relaybuttonpins = [20,21,22,23] #to buttons
    for i in lightbuttonpins:
        GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    for i in relaybuttonpins:
        GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    for i in relaybuttonpins_r:
        GPIO.setup(i, GPIO.OUT,initial=0)
    light_ser_out={
        'start': 8,
        'headlights': 0,
        'left_ind': 4,
        'right_ind': 6,
        'hazard': 2,
        'brake': 10,
        }
    buttonmap = {
        4:'start',
        5:'headlights',
        6:'left_ind',
        7:'right_ind',
        8:'hazard',
        9:'brake',
        10:'clutch',
        11:'lap_count',
        12:'ptt',
        20:'horn',
        21:'wiper'
    } 
    accessory_controller_dict = {
        'type':'accessory_controller',
        'cloud':False,
        'start': False,
        'headlights': False,
        'left_ind': False,
        'right_ind': False,
        'hazard': False,
        'brake': False,
        'clutch': False,
        'lap_count': False,
        'ptt': False,
        'horn': False,
        'wiper': False,
    } 
    acc_prev = {
        'type':'accessory_controller',
        'start': False,
        'headlights': False,
        'left_ind': False,
        'right_ind': False,
        'hazard': False,
        'brake': False,
        'clutch': False,
        'lap_count': False,
        'ptt': False,
        'horn': False,
        'wiper': False,
    } 
    

    def light_callback(channel):
        global time_stamp
        time_now=time.time()
        ser_cmd=['A','B','C','D','E','F','G','H','I','J','K','L']
        if(time_now-time_stamp)>= 0.3:
            if channel==4 or 5 or 6 or 7 or 8 or 9:
                time_stamp=time.time()
                button=buttonmap[channel]
                accessory_controller_dict[button]= not accessory_controller_dict[button]
                on_off=int(accessory_controller_dict[button])
                send=ser_cmd[(int(light_ser_out[button])+on_off)]
                ard.write(b'%s' %(send,))
                acc_prev[button]=accessory_controller_dict[button]
                print(button, accessory_controller_dict[button], on_off)
                print (button, send)
        

    
    def relay_callback(channel):
        global time_stamp
        time_now=time.time()
        if (time_now-time_stamp)>= 0.3:
            time_stamp=time.time()
            button=buttonmap[channel]
            accessory_controller_dict[button]= not accessory_controller_dict[button]
            relay_pin=int(channel)-4
            GPIO.output(relay_pin,accessory_controller_dict[button])
            acc_prev[button]=accessory_controller_dict[button]
            print(button, accessory_controller_dict[button])

    def cloudhandle():
        accessory_controller_dict['cloud']=False
        ser_cmd=['A','B','C','D','E','F','G','H','I','J','K','L']
        for acc in accessory_controller_dict:
            for prev in acc_prev.iterkeys():
                if acc==prev and accessory_controller_dict[acc] != acc_prev[acc]:
                    for button,item in buttonmap.iteritems():
                        if item == acc and button == 4 or 5 or 6 or 7 or 8 or 9:
                            on_off=int(accessory_controller_dict[acc])
                            #send=int(light_ser_out[acc])+on_off
                            send=ser_cmd[(int(light_ser_out[button])+on_off)]
                            ard.write(b'%d' %(send,))
                            acc_prev[acc]=accessory_controller_dict[acc]
                        if item == acc and button == 20 or 21 or 22 or 23:
                            GPIO.output(button-4,int(accessory_controller_dict[button]))
                            acc_prev[acc]=accessory_controller_dict[acc]
                
        
                        
    for i in lightbuttonpins:
        GPIO.add_event_detect(i, GPIO.FALLING, callback=light_callback)
    for i in relaybuttonpins:
        GPIO.add_event_detect(i, GPIO.BOTH, callback=relay_callback)

    while True:
        time_now=time.time()
        if accessory_controller_dict['cloud']==True:
            cloudhandle()
        if (time_now-time_speed)>=2:   
            ard.write(b'S')
            time_speed=time.time()
        if ard.in_waiting>0: #response is speed from gps
            response=ard.readline()
            print (response)

run()