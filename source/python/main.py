#!/usr/bin/env python3
import os
import sys
from datetime import datetime
import modules.gui_elements as gui_elements
from threading import Thread
from modules.updater import Updater
from modules.usb_detector import USBHotplugDetector
from modules.file_operations_provider import FileOperationsProvider

ENVIRONMENTAL_VARIABLES = ['DEVS_MOUNTPOINT', 'LOGS_DIRECTORY_PATH', 'TESTING_PORTS']

class Main():
    def main(self):
        try:
            if len(sys.argv) == 1:
                print('File requires at least one console argument.')
            else:
                print('Checking for updates...')

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
    
    def __check_for_update(self):
        os.chdir('../../')

        self.core_framework_location = os.path.abspath(os.curdir)
        self.last_update_file_location = self.core_framework_location + '/source/python/update_logs/last_update_date.log'
        self.versions_log_file = self.core_framework_location + '/source/python/update_logs/versions.json'

        if not os.path.isfile(self.last_update_file_location):
            with open(self.last_update_file_location, 'w'):
                print('>>> Created empty last_updated.log')
            
        if not os.path.isfile(self.versions_log_file):
            with open(self.versions_log_file, 'w'):
                print('>>> Created empty versions.json')

        with open(self.last_update_file_location) as last_update_date:
            last_update_date =  last_update_date.read()

        if last_update_date == '' or last_update_date != datetime.now().strftime('%b %d %Y'):
            print('>>> Updating.')
            if self.__update():
                print('>>> Update was successful.')
        else:
            print('>>> Update date is not reached yet.')
    
    def __update(self):
        updater = Updater(
                self.core_framework_location,
                'https://tdbrknxrgf.execute-api.us-east-1.amazonaws.com/dev/update'
            )

        update_result = updater.update()
            
        if not update_result:
            return False
        else:
            with open(self.last_update_file_location, 'w') as last_update_date:
                last_update_date.write(str(datetime.now().strftime('%b %d %Y')))
    
            updater.restart_parent()
if __name__ == '__main__':
    Main().validate_env_variables()
    Main().main()
