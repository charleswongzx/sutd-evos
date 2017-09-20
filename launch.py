from multiprocessing import Process

import lcm
import kivy

import modules.dashboard_buttons
import modules.dashboard_display
import modules.telemetry_storage
import modules.accessory_control
import modules.camera_reader
import modules.efi_parser
import modules.web_bridge

def main():

    # TODO: initiate program launch sequence
    # TODO: error check and monitor status

    procs = []

    dashboard_buttons_proc = Process(target=dashboard_buttons)
    dashboard_buttons_proc = Process(target=dashboard_display)
    telemetry_storage_proc = Process(target=telemetry_storage)
    accessory_control_proc = Process(target=accessory_control)
    camera_reader_proc = Process(target=camera_reader)
    efi_parser_proc = Process(target=efi_parser)
    web_bridge_proc = Process(target=web_bridge)

    return 1

if __name__ == '__main__':
    main()
