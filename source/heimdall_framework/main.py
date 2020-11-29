#!/usr/bin/env python3
import os
import sys
import shutil
import argparse
from datetime import datetime
from .modules import gui_elements
from .modules.logger import Logger
from .modules.updater import Updater
from .modules.usb_detector import USBHotplugDetector
from .modules.file_operations_provider import FileOperationsProvider
from .modules.configuration_deserializer import ConfigurationDeserializer

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
            nargs='?',
            help='Indicates whether the GUI will be initialized or not.',
            )
        parser.add_argument(
            '--screen',
            nargs='?',
            type=str,
            help='The GUI mode. Should be "normal", "fullscreen" or left empty.',
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
        framework_location = os.path.abspath(os.path.join(current_file_location, '../../'))

        logger.log('Initiating updater')
        updater = Updater(
            configuration, 
            logger, 
            framework_location,
            ''
            )

        logger.log('Checking for updates.')
        if updater.can_update(logger):
            updater.update(logger)
        
        logger.log('Initiating USB hotplug detector.')
        if cli_arguments.interface == None or cli_arguments.interface == 'nogui':
            usb_detector = USBHotplugDetector(configuration, logger)
            usb_detector.start()
        else:
            if cli_arguments.screen == None or cli_arguments.screen == 'normal':
                gui_elements.show_gui(configuration, logger, False)
            else:
                gui_elements.show_gui(configuration, logger, True)

def run(): 
    Main().main()