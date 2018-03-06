import serial
import time
import RPi.GPIO as GPIO

time_stamp=time.time()

time_speed=time.time()



def run():
    global time_speed
    engine_toggle=False
    time_stamp=time.time()
    ard=serial.Serial('/dev/ttyACM0',115200)
    GPIO.setmode(GPIO.BCM)
    lightbuttonpins = [5,6,7,8]
    relaybuttonpins_r=[16,17,18,19,24] #to relay 16 horn 17 wiper 18 led light 19 close 24 cut
    relaybuttonpins = [20,21,22,9,10] #to buttons
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
        22:'start',
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
    ax_control_dict = {
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
    ax_prev = {
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
            if channel==5 or 6 or 7 or 8:
                time_stamp=time.time()
                button=buttonmap[channel]
                ax_control_dict[button]= not ax_control_dict[button]
                on_off=int(ax_control_dict[button])
                send=ser_cmd[(int(light_ser_out[button])+on_off)]
                ard.write(b'%s' %(send,))
                ax_prev[button]=ax_control_dict[button]
                print(button, ax_control_dict[button], on_off)
                print (button, send)
        

    
    def relay_callback(channel):
        global time_stamp
        time_now=time.time()
        ser_cmd=['A','B','C','D','E','F','G','H','I','J','K','L']
        if (time_now-time_stamp)>= 0.15:
            #if starter button pushed
            if (channel==22 and ax_control_dict['clutch'] == True):
                time_stamp=time.time()
                button=buttonmap[channel]
                ax_control_dict[button]= not ax_control_dict[button]

                #relay controls, 18 led lights, 19 solenoid, 24 kill ecu
                if engine_toggle == False:
                    if ax_control_dict[button]== True:
                        #solenoid toggle
                        GPIO.output(19,GPIO.HIGH)
                        #lights for starter
                        on_off=int(ax_control_dict[button])
                        send=ser_cmd[(int(light_ser_out[button])+on_off)]
                        ard.write(b'%s' %(send,))
                        GPIO.output(18,ax_control_dict[button])
                    elif ax_control_dict[button] == False:
                        #Solenoid off
                        GPIO.output(19,GPIO.LOW)
                        #lights off for starter
                        on_off=int(ax_control_dict[button])
                        send=ser_cmd[(int(light_ser_out[button])+on_off)]
                        ard.write(b'%s' %(send,))
                        #enable LED colour swap
                        GPIO.output(18, ax_control_dict[button])
                elif engine_toggle == True:
                    GPIO.output(24,GPIO.HIGH)
                    GPIO.output(18,GPIO.LOW)
                    engine_toggle==False
            elif (channel == 9): #brake lights
                time_stamp=time.time()
                button=buttonmap[channel]
                ax_control_dict[button]= not ax_control_dict[button]
                on_off=int(ax_control_dict[button])
                send=ser_cmd[(int(light_ser_out[button])+on_off)]
                ard.write(b'%s' %(send,))
                ax_prev[button]=ax_control_dict[button]                
            elif (channel == 20, 21): #horn,wiper
                time_stamp=time.time()
                button=buttonmap[channel]
                ax_control_dict[button]= not ax_control_dict[button]
                relay_pin=int(channel)-4
                GPIO.output(relay_pin,ax_control_dict[button])
                ax_prev[button]=ax_control_dict[button]
        print(button, ax_control_dict[button])
        print (button, send)
                    

    def cloudhandle():
        ax_control_dict['cloud']=False
        ser_cmd=['A','B','C','D','E','F','G','H','I','J','K','L']
        for acc in ax_control_dict:
            for prev in ax_prev.iterkeys():
                if acc==prev and ax_control_dict[acc] != ax_prev[acc]:
                    for button,item in buttonmap.iteritems():
                        if item == acc and button == 4 or 5 or 6 or 7 or 8 or 9:
                            on_off=int(ax_control_dict[acc])
                            #send=int(light_ser_out[acc])+on_off
                            send=ser_cmd[(int(light_ser_out[button])+on_off)]
                            ard.write(b'%d' %(send,))
                            ax_prev[acc]=ax_control_dict[acc]
                        if item == acc and button == 20 or 21 or 22:
                            GPIO.output(button-4,int(ax_control_dict[button]))
                            ax_prev[acc]=ax_control_dict[acc]
                
        
                        
    for i in lightbuttonpins:
        GPIO.add_event_detect(i, GPIO.FALLING, callback=light_callback)
    for i in relaybuttonpins:
        if i==1:
            GPIO.add_event_detect(i,GPIO.FALLING, callback=relay_callback)# wiper for momentary
        else:
            GPIO.add_event_detect(i, GPIO.BOTH, callback=relay_callback)

    while True:
        time_now=time.time()
        if ax_control_dict['cloud']==True:
            cloudhandle()
        if (time_now-time_speed)>=2:   
            ard.write(b'S')
            time_speed=time.time()
        if ard.in_waiting>0: #response is speed from gps
            response=ard.readline()
            print (response)

run()