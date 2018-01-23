import websocket
import thread
import json
import time
import select

import lcm
from exlcm import ax_control_t
from exlcm import veh_status_t
from exlcm import log_control_t
from exlcm import cam_feed_t
from exlcm import eng_toggle_t
from exlcm import lap_count_t


def run():

    debug = False

    lap_count_dict = {'type': 'lap_count',
                      'current_lap': 0}

    eng_toggle_dict = {'type': 'eng_toggle',
                       'toggle': False}

    veh_status_dict = {'type': 'engine_stat',
                       'timestamp': time.clock(),
                       'running': False,
                       'rpm': 0,
                       'speed': 0,
                       'temp': 0,
                       'fuel_flow': 0,
                       'pressure': 0}

    log_control_dict = {'timestamp': time.clock(),
                        'type': '',
                        'recording': False}

    ax_control_dict = {'type': 'ax_control',
                       'timestamp': time.clock(),
                       'source': 'nil', # nil, ax_controller or web
                       'wipers': False,
                       # 'ptt': False,
                       'horn': False,
                       'headlight': False,
                       'sig_l': False,
                       'sig_r': False,
                       'brake': False,
                       'hazard': False
                       }

    cam_dict = {'frame': bytearray(),
                'running': False
                }

    # LCM Handling
    def eng_toggle_handler(channel, data):
        msg = eng_toggle_t.decode(data)
        eng_toggle_dict['toggle'] = msg.toggle

    def lap_count_handler(channel, data):
        msg = lap_count_t.decode(data)
        lap_count_dict['current_lap'] = msg.current_lap

    def cam_feed_handler(channel, data):
        msg = cam_feed_t.decode(data)
        cam_dict['running'] = msg.feed_running
        cam_dict['frame'] = msg.frame

    def ax_control_handler(channel, data):
        msg = ax_control_t.decode(data)
        ax_control_dict['source'] = msg.source
        ax_control_dict['wipers'] = msg.wipers
        # ax_control_dict['ptt'] = msg.ptt
        ax_control_dict['headlight'] = msg.headlight
        ax_control_dict['horn'] = msg.horn
        ax_control_dict['sig_l'] = msg.sig_l
        ax_control_dict['sig_r'] = msg.sig_r
        ax_control_dict['brake'] = msg.brake
        ax_control_dict['hazard'] = msg.hazard

    def eng_status_handler(channel, data):
        # global veh_status_dict
        msg = veh_status_t.decode(data)
        veh_status_dict['timestamp'] = time.clock()
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

    # LCM object and subscriptions
    lc = lcm.LCM()
    eng_sub = lc.subscribe("eng_status", eng_status_handler)
    cam_sub = lc.subscribe("cam_feed", cam_feed_handler)
    ax_sub = lc.subscribe("ax_control", ax_control_handler)

    # Websockets
    def on_message(ws, message):
        print(message)

    def on_error(ws, error):
        print(error)

    def on_close(ws):
        print ('Connection to EVOS_WEB closed.')

    def on_open(ws):
        print('Connection to EVOS_WEB established.')

        def send_video_frame(frame):
            return ws.send(b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        def runner(*args):
            # global veh_status_dict

            print('Websocket runner started.')

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
                        if cam_dict['running'] and old_frame != cam_dict['frame']:
                            send_video_frame(cam_dict['frame'])
                            old_frame = cam_dict['frame']

                        # Vehicle status
                        veh_status_json = json.dumps(veh_status_dict)
                        ws.send(veh_status_json)

                        # Engine toggle
                        ws.send(json.dumps(eng_toggle_dict))

                        # Lap Count
                        ws.send(json.dumps(lap_count_dict))

                    else:
                        if debug:
                            print("Message queue empty...")

            except KeyboardInterrupt:
                ws.close()
                pass

            except websocket.WebSocketConnectionClosedException:
                pass

        thread.start_new_thread(runner, ())

    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://127.0.0.1:8000/",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.on_open = on_open
    while True:
        try:
            ws.run_forever()
            print 'Attempting to reconnect in 5s...'
            time.sleep(5)

        except KeyboardInterrupt:
            pass

run()
