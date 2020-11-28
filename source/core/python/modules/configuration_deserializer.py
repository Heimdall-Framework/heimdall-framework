import os
import json
from plugypy import Plugin
from plugypy import Configuration as PluginsConfiguration 

class FrameworkConfiguration(object):
    logs_directory: str
    mounting_point: str
    updates_intensity: str
    testing_ports: list(int)
    nuking_ports: list(int)
    plugins_config: PluginsConfiguration

    def __init__(self, logs_directory: str, mounting_point: str, updates_intensity: str, testing_ports: [int], nuking_ports: [int], plugins_config: PluginsConfiguration):
        self.logs_directory = logs_directory
        self.mounting_point = mounting_point
        self.updates_intensity = updates_intensity
        self.testing_ports = testing_ports
        self.nuking_ports = nuking_ports
        self.plugins_config = plugins_config

    def set_plugins_configuration(self, plugins):
        pass

class ConfigurationDeserializer():
    def __init__(self, config_file_location):
        self.__config_file_location = config_file_location
    
    def deserialize(self):
        configuration_json = None
        configuration = None
        
        try:
            with open(self.__config_file_location, 'r') as configuration_file:
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