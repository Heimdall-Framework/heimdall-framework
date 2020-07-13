#!/usr/bin/env python3
import os
import sys
import modules.gui_elements as gui_elements
from threading import Thread
from modules.usb_detector import USBHotplugDetector
from modules.file_operations_provider import FileOperationsProvider

ENVIRONMENTAL_VARIABLES = ['DEVS_MOUNTPOINT', 'LOGS_DIRECTORY_PATH', 'TESTING_PORTS']

class Main():
    def main(self):
        try:
            if len(sys.argv) == 1:
                print('File requires at least one console argument.')
            else:
                if sys.argv[1].lower() == 'gui':    
                    gui_elements.show_gui()

                elif sys.argv[1].lower() == 'nogui':
                    usb_detector = USBHotplugDetector()
                    usb_detector.start()
        except KeyboardInterrupt:
            print('Keyboard interrupt detected.')
    
    def validate_env_variables(self):
        try:
            os.environ['SUDO_UID']
        except KeyError:
            print('Please start the application using "sudo -E".')
        
        for env_variable in ENVIRONMENTAL_VARIABLES:
            try:
                os.environ[env_variable]
            except KeyError:
                print('Environmental variable {} is not set.'.format(env_variable))
        
if __name__ == '__main__':
    Main().validate_env_variables()
    Main().main()
