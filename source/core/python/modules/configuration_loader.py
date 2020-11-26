import os
import json

class Configuration(object):
    logs_directory: str
    mounting_point: str
    updates_intensity: str
    testing_ports: list(int)
    nuking_ports: list(int)

    def __init__(self, logs_directory, mounting_point, updates_intensity, testing_ports, nuking_ports):
        self.logs_directory = logs_directory
        self.mounting_point = mounting_point
        self.updates_intensity = updates_intensity
        self.testing_ports = testing_ports
        self.nuking_ports = nuking_ports

class ConfigurationLoader():
    def __init__(self, config_file_location):
        self.__config_file_location = config_file_location
    
    def load(self):
        configuration_json = None
        configuration = None
        
        try:
            with open(self.__config_file_location, 'r') as configuration_file:
                configuration_json = configuration_file.read()
            
            loaded_json = json.loads(configuration_json)
            configuration = Configuration(**loaded_json)
        except FileNotFoundError as file_not_found_error:
            print('>>> Configuration file was not found on it\'s default location.')
            print('>>> {}'.format(file_not_found_error))
        except ValueError as value_error:
            print('>>> Invalid configuration file format.')
            print('>>> {}'.format(value_error))
        
        return configuration