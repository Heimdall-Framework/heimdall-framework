#!/usr/bin/env python3
import os
import sys
import shutil
from datetime import datetime
import modules.gui_elements as gui_elements
from modules.logger import Logger
from modules.updater import Updater
from modules.usb_detector import USBHotplugDetector
from modules.file_operations_provider import FileOperationsProvider

ENVIRONMENTAL_VARIABLES = ['DEVS_MOUNTPOINT', 'LOGS_DIRECTORY_PATH', 'TESTING_PORTS', 'NUKING_PORTS']

class Main():
    def main(self) -> None:
        try:
            if len(sys.argv) == 1:
                Logger().log('File requires at least one console argument.')
            else:
                Logger().log('Checking for updates...')
                self.__check_for_update()

                if sys.argv[1].lower() == 'gui':
                    if sys.argv[2].lower() == '--normal':
                        gui_elements.show_gui(False)
                    else:
                        gui_elements.show_gui(True)

                elif sys.argv[1].lower() == 'nogui':
                    usb_detector = USBHotplugDetector()
                    usb_detector.start()

        except KeyboardInterrupt:
            Logger().log('Keyboard interrupt detected.')
    
    def validate_env_variables(self) -> None:
        try:
            os.environ['SUDO_UID']
        except KeyError:
            Logger().log('Please start the application using "sudo -E".')
        
        for env_variable in ENVIRONMENTAL_VARIABLES:
            try:
                os.environ[env_variable]
            except KeyError:
                Logger().log('Environmental variable {} is not set.'.format(env_variable))
    
    def __check_for_update(self) -> None:
        '''
        Check if any new updates are available.
        '''
        self.core_framework_location = os.path.abspath(os.path.join(os.path.dirname( __file__), '../../../')) 
        self.last_update_file_location = self.core_framework_location + '/source/core/python/update_logs/last_update_date.log'
        self.versions_log_file = self.core_framework_location + '/source/core/python/update_logs/versions.json'

        if not os.path.isfile(self.last_update_file_location):
            with open(self.last_update_file_location, 'w'):
                Logger().log('>>> Created empty last_updated.log')
            
        if not os.path.isfile(self.versions_log_file):
            with open(self.versions_log_file, 'w'):
                Logger().log('>>> Created empty versions.json')

        with open(self.last_update_file_location) as last_update_date:
            last_update_date =  last_update_date.read()

        if last_update_date == '' or last_update_date != datetime.now().strftime('%b %d %Y'):
            Logger().log('>>> Updating.')
            if self.__update():
                Logger().log('>>> Update was successful.')
        else:
            Logger().log('>>> Update date is not reached yet.')
    
    def __update(self) -> None:
        '''
        Update the framework on the device.
        '''
        updater = Updater(
                self.core_framework_location,
                'https://vio1hjlpx9.execute-api.eu-central-1.amazonaws.com/dev/update'
            )

        update_result = updater.update()
            
        if not update_result:
            return False
        else:
            with open(self.last_update_file_location, 'w') as last_update_date:
                last_update_date.write(str(datetime.now().strftime('%b %d %Y')))
    
            updater.restart_parent()

def main():             
    Main().validate_env_variables()
    Main().main()

main()