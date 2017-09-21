import multiprocessing as mp

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

    # TODO: error check and monitor status

    # Init processes
    procs = []

    dash_buttons_proc = mp.Process(target=dash_buttons.run)
    dash_display_proc = mp.Process(target=dash_display)
    tele_storage_proc = mp.Process(target=tele_storage)
    ax_control_proc = mp.Process(target=ax_controller)
    cam_reader_proc = mp.Process(target=cam_reader)
    efi_parser_proc = mp.Process(target=efi_parser)
    web_bridge_proc = mp.Process(target=web_bridge)

    # Store and run processes
    procs.append(dash_buttons_proc)
    procs.append(dash_display_proc)
    procs.append(tele_storage_proc)
    procs.append(ax_control_proc)
    procs.append(cam_reader_proc)
    procs.append(efi_parser_proc)
    procs.append(web_bridge_proc)

    for process in procs:
        process.start()

    return 1


if __name__ == '__main__':
    print 'Launching main process...'
    main()
