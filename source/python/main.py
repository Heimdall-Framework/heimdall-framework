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

        self.validate_env_variables()    
   
        if sys.argv[1] == 'GUI':
            gui_elements.show_gui()

        elif sys.argv[1] == 'NOGUI':
            usb_detector = USBHotplugDetector()
            usb_detector.start()
    
    def validate_env_variables(self):
        try:
            os.environ['DEVS_MOUNTPOINT']
            os.environ['DUMPS_DIRECTORY_PATH']
        except:
            print('Environmental variable has not been set.')
        
if __name__ == '__main__':
    Main().main()
