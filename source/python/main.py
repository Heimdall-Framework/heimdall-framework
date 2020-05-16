#!/usr/bin/env python3
import os
import sys
import gui_elements
from threading import Thread
from usb_detector import USBHotplugDetector
from file_operations_provider import FileOperationsProvider

class Main():
    def main(self):
        if len(sys.argv) == 0:
            print('File requires one console argument.')

        if sys.argv[1].lower() == 'gui':    
            gui_elements.show_gui()

        elif sys.argv[1].lower() == 'nogui':
            usb_detector = USBHotplugDetector()
            usb_detector.start()
    
    def validate_env_variables(self):
        try:
            os.environ['DEVS_MOUNTPOINT']
            os.environ['LOGS_DIRECTORY_PATH']
            os.environ['TESTING_PORT']
        except KeyError:
            print('One or more environmental variables have not been set or exported correctly.')
            raise
        try:
            os.environ['SUDO_UID']
        except KeyError:
            print('Please start the application using "sudo -E".')
            raise
        
if __name__ == '__main__':
    Main().validate_env_variables()
    Main().main()
