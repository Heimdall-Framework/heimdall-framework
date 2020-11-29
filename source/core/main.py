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
    def __init__(self):
        pass

    def main(self) -> None:
        configuration_deserializer = None
        configuration = None
        
        parser = argparse.ArgumentParser(description='Load CLI flags for the framework.')
        parser.add_argument(
            '--config',
            type=str,
            help='Path to your custom configuration file. If no passed, will load the default one.'
            )
        parser.add_argument(
            '--interface', 
            type=str,
            help='Indicates whether the GUI will be initialized or not.',
            )

        cli_arguments = parser.parse_args()

        if cli_arguments.interface == None:
            print('Interface must be specified.')
            return

        print('Loading configuration')
        if cli_arguments.config != None:
            configuration_deserializer = ConfigurationDeserializer(cli_arguments.config)
            configuration = configuration_deserializer.deserialize()

        configuration_deserializer = ConfigurationDeserializer('../configuration.json')
        configuration = configuration_deserializer.deserialize()

        logger = Logger(configuration.logs_directory)

        current_file_location = os.path.dirname(os.path.abspath(__file__))
        framework_location = os.path.abspath(current_file_location, '../../')

        logger.log('Initiating updater')
        updater = Updater(
            configuration, 
            logger, 
            framework_location,
            ''
            )

        if sys.argv[1].lower() == 'gui':
            if sys.argv[2].lower() == '--normal':
                gui_elements.show_gui(configuration, False)
            else:
                gui_elements.show_gui(configuration, True)

        elif sys.argv[1].lower() == 'nogui':
            usb_detector = USBHotplugDetector(configuration)
            usb_detector.start()
    
    
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

if __name__=='__main__':       
    Main().main()