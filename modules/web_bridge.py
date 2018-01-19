import websocket
import thread
import json
import time
import select

import lcm
from exlcm import ax_control_t
from exlcm import eng_status_t
from exlcm import log_control_t
from exlcm import cam_feed_t

def run():
    running = False
    rpm = 0
    speed = 0
    temp = 0
    fuel_flow = 0
    pressure = 0

    veh_status_dict = {'type': 'engine_stat',
                       'timestamp': 0,
                       'running': running,
                       'rpm': rpm,
                       'speed': speed,
                       'temp': temp,
                       'fuel_flow': fuel_flow,
                       'pressure': pressure}

    log_control_dict = {'timestamp': 0,
                        'type': '',
                        'recording': False}

    cam_frame = bytearray()
    cam_running = False

    # LCM Handling
    def cam_feed_handler(channel, data):
        msg = cam_feed_t.decode(data)
        cam_running = msg.feed_running
        cam_frame = msg.frame


    def ax_control_handler(channel, data):
        msg = ax_control_t.decode(data)
        print msg.source

    def eng_status_handler(channel, data):
        # global veh_status_dict
        msg = eng_status_t.decode(data)
        # veh_status_dict['timestamp'] = time.clock()
        veh_status_dict['running'] = msg.running
        veh_status_dict['rpm'] = msg.rpm
        veh_status_dict['speed'] = msg.speed
        veh_status_dict['temp'] = msg.temp
        veh_status_dict['fuel_flow'] = msg.fuel_flow
        veh_status_dict['pressure'] = msg.pressure

    def log_control_handler(channel, data):
        global log_control_dict
        msg = log_control_t.decode(data)
        log_control_dict['timestamp'] = time.clock()
        log_control_dict['recording'] = msg.recording

        if msg.recording:
                log_control_dict['type'] = 'log_begin'
        else:
            log_control_dict['type'] = 'log_end'


    lc = lcm.LCM()
    eng_sub = lc.subscribe("eng_status", eng_status_handler)

    # Websockets
    def on_message(ws, message):
        print(message)

    def on_error(ws, error):
        print(error)

    def on_close(ws):
        print("### closed ###")

    def on_open(ws):
        def send_video_frame(frame):
            return None

        def runner(*args):
            # global veh_status_dict

            print('websocket runner started')

            try:
                # to prevent sending duplicates
                old_veh_status_dict = {}
                old_frame = bytearray()

                while True:
                    rfds, wfds, efds = select.select([lc.fileno()], [], [], 1.5)
                    if rfds:
                        lc.handle()
                        # Log recording
                        # log_record_json = json.dumps(log_record_dict)
                        # ws.send(log_record_json)

                        # Camera feed
                        if cam_running and old_frame != cam_frame:
                            ws.send(b'--frame\r\n'
                                    b'Content-Type: image/jpeg\r\n\r\n' + cam_frame + b'\r\n')
                            old_frame = cam_frame

                        # Vehicle status
                        if cmp(veh_status_dict, old_veh_status_dict):
                            veh_status_json = json.dumps(veh_status_dict)
                            ws.send(veh_status_json)
                            old_veh_status_dict = veh_status_dict.copy()
                    else:
                        print("Message queue empty...")

            except KeyboardInterrupt:
                    ws.close()
                    pass

            # while True:
            #     try:
            #         lc.handle()
            #         print (lc.fileno())
            #         print('lcm handled')
            #
            #         # # Log recording
            #         # log_record_json = json.dumps(log_record_dict)
            #         # ws.send(log_record_json)
            #
            #         # Vehicle status
            #         veh_status_json = json.dumps(veh_status_dict)
            #         ws.send(veh_status_json)
            #
            #         time.sleep(0.08)  # 12Hz
            #
            #     except KeyboardInterrupt:
            #         ws.close()
            #         pass

        thread.start_new_thread(runner, ())

    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://127.0.0.1:8000/",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()

run()
