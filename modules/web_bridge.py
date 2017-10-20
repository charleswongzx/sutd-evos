import websocket
import thread
import json
import time

import lcm
from exlcm import ax_control_t
from exlcm import eng_status_t


def run():
    running = False
    rpm = 0
    speed = 0
    temp = 0
    fuel_flow = 0
    pressure = 0

    veh_status_dict = {'type': 'engine_stat',
                       'timestamp': time.clock(),
                       'running': running,
                       'rpm': rpm,
                       'speed': speed,
                       'temp': temp,
                       'fuel_flow': fuel_flow,
                       'pressure': pressure}

    # LCM Handling
    def ax_handler(channel, data):
        msg = ax_control_t.decode(data)
        print msg.source

    def eng_handler(channel, data):
        global veh_status_dict
        msg = eng_status_t.decode(data)
        veh_status_dict['timestamp'] = time.clock()
        veh_status_dict['running'] = msg.running
        veh_status_dict['rpm'] = msg.rpm
        veh_status_dict['speed'] = msg.speed
        veh_status_dict['temp'] = msg.temp
        veh_status_dict['fuel_flow'] = msg.fuel_flow
        veh_status_dict['pressure'] = msg.pressure

    lc = lcm.LCM()
    eng_sub = lc.subscribe("eng_status", eng_handler)

    # Websockets
    def on_message(ws, message):
        print(message)

    def on_error(ws, error):
        print(error)

    def on_close(ws):
        print("### closed ###")

    def on_open(ws):
        def runner(*args):
            global veh_status_dict

            while True:
                try:
                    lc.handle()

                    # Log recording
                    log_record_json = json.dumps(log_record_dict)
                    ws.send(log_record_json)

                    # Vehicle status
                    veh_status_json = json.dumps(veh_status_dict)
                    ws.send(veh_status_json)

                    time.sleep(0.08)  # 12Hz

                except KeyboardInterrupt:
                    ws.close()
                    pass

        thread.start_new_thread(runner, ())

    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://127.0.0.1:8000/",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()

run()
