from multiprocessing import Process

import lcm
import kivy

import modules.dashboard_buttons as dash_buttons
import modules.dashboard_display as dash_display
import modules.telemetry_storage as tele_storage
import modules.accessory_controller as ax_controller
import modules.camera_reader as cam_reader
import modules.efi_parser as efi_parser
import modules.web_bridge as web_bridge


def main():

    # TODO: initiate program launch sequence
    # TODO: error check and monitor status

    procs = []

    dashboard_buttons_proc = Process(target=dash_buttons.run)
    dashboard_buttons_proc = Process(target=dash_display)
    telemetry_storage_proc = Process(target=tele_storage)
    accessory_control_proc = Process(target=ax_controller)
    camera_reader_proc = Process(target=cam_reader)
    efi_parser_proc = Process(target=efi_parser)
    web_bridge_proc = Process(target=web_bridge)

    return 1


if __name__ == '__main__':
    print 'Launching main process...'
    main()
