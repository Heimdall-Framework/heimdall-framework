import os
import json
from .framework_configuration import FrameworkConfiguration
from plugypy import Plugin
from plugypy import Configuration as PluginsConfiguration 

class ConfigurationDeserializer():
    def __init__(self, config_file_location):
        self._config_file_location = config_file_location
    
    def deserialize(self):
        configuration_json = None
        configuration = None
        
        try:
            with open(self._config_file_location, 'r') as configuration_file:
                configuration_json = configuration_file.read()
            
            loaded_json = json.loads(configuration_json)
            configuration = FrameworkConfiguration(**loaded_json)

        except FileNotFoundError as file_not_found_error:
            print('>>> Configuration file was not found on it\'s default location.')
            print('>>> {}'.format(file_not_found_error))
        except ValueError as value_error:
            print('>>> Invalid configuration file format.')
            print('>>> {}'.format(value_error))
        
        return configuration