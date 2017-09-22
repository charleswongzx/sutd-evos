import multiprocessing as mp
from ConfigParser import SafeConfigParser

import lcm

import modules.dashboard_buttons as dash_buttons
import modules.dashboard_display as dash_display
import modules.telemetry_storage as tele_storage
import modules.accessory_controller as ax_controller
import modules.camera_reader as cam_reader
import modules.efi_parser as efi_parser
import modules.web_bridge as web_bridge


def main():


    # Reading config file
    config = SafeConfigParser()
    config.read('config/evos_config.ini')

    verbose = config.get('main', 'verbose')  # Follow this structure to pull options from config file

    # Init processes
    procs = []

    dash_buttons_proc = mp.Process(target=dash_buttons.run, name='dash_buttons_proc')
    dash_display_proc = mp.Process(target=dash_display.run, name='dash_display_proc')
    tele_storage_proc = mp.Process(target=tele_storage.run, name='tele_storage_proc')
    ax_control_proc = mp.Process(target=ax_controller.run, name='ax_control_proc')
    cam_reader_proc = mp.Process(target=cam_reader.run, name='cam_reader_proc')
    efi_parser_proc = mp.Process(target=efi_parser.run, name='efi_parser_proc')
    web_bridge_proc = mp.Process(target=web_bridge.run, name='web_bridge_proc')

    # Store and run processes
    procs.append(dash_buttons_proc)
    procs.append(dash_display_proc)
    procs.append(tele_storage_proc)
    procs.append(ax_control_proc)
    procs.append(cam_reader_proc)
    procs.append(efi_parser_proc)
    procs.append(web_bridge_proc)

    for process in procs:
        if verbose == 'true':
            print 'Starting', process.name
        process.start()

    for process in procs:
        # End processes gracefully
        process.join()

        # TODO Kill processes (perhaps with KeyboardInterrupt)
        process.terminate()



    return 1


if __name__ == '__main__':
    print 'Launching EVOS...'
    main()
