#!/usr/bin/env python3
import os
import sys
import shutil
import argparse
from datetime import datetime
import modules.gui_elements as gui_elements
from modules.logger import Logger
from modules.updater import Updater
from modules.usb_detector import USBHotplugDetector
from modules.file_operations_provider import FileOperationsProvider
from modules.configuration_deserializer import ConfigurationDeserializer

class Main():
    def main(self) -> None:
        parser = argparse.ArgumentParser(description='Load CLI flags for the framework.')
        parser.add_argument('--config',type=str, help='Path to your custom configuration file. If no passed, will load the default one.')
        parser.add_argument('--interface', type=str, help='Indicates whether the GUI will be initialized or not.')

        cli_arguments = parser.parse_args()

        if cli_arguments.interface == '':
            Logger().log('Interface must be specified.')
            return

        Logger().log('Loading configuration')
        configuration_deserializer = ConfigurationDeserializer('../configuration.json')
        configuration = configuration_deserializer.deserialize()

        Logger().log('Checking for updates...')
        self.__check_for_update(configuration)

        if sys.argv[1].lower() == 'gui':
            if sys.argv[2].lower() == '--normal':
                gui_elements.show_gui(configuration, False)
            else:
                gui_elements.show_gui(configuration, True)

        elif sys.argv[1].lower() == 'nogui':
            usb_detector = USBHotplugDetector(configuration)
            usb_detector.start()
    
    def __check_for_update(self, configuration) -> None:
        '''
        Check if any new updates are available.
        '''
        
        self.core_framework_location = os.path.abspath(os.path.join(os.path.dirname( __file__), '../../../')) 
        self.last_update_file_location = self.core_framework_location + '/source/core/python/update_logs/last_update_date.log'
        self.versions_file_location = self.core_framework_location + '/source/core/python/update_logs/versions.json'

        if not os.path.isfile(self.last_update_file_location):
            with open(self.last_update_file_location, 'w'):
                Logger().log('>>> Created empty last_updated.log')
            
        if not os.path.isfile(self.versions_file_location):
            with open(self.versions_file_location, 'w'):
                Logger().log('>>> Created empty versions.json')

        with open(self.last_update_file_location) as last_update_date:
            last_update_date =  last_update_date.read()
        
        if configuration.updates_intensity == 'normal':
            if not (last_update_date == '' or last_update_date != datetime.now().strftime('%b %d %Y')):
                Logger().log('>>> Update date is not reached yet.')
                return

        Logger().log('>>> Updating.')
        if self.__update():
            Logger().log('>>> Update was successful.')
            
    
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
    Main().main()

main()