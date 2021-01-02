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
            configuration_file_contents = self.__read_configuration_file()
            configuration_json = json.loads(configuration_file_contents)

            configuration = FrameworkConfiguration(**loaded_json)

        except ValueError as value_error:
            print('>>> Invalid configuration file format.')
            print('>>> {}'.format(value_error))

        return configuration

    def __decode_configuration(self, configuration_json) -> FrameworkConfiguration:
        plugins = list()
        for plugin in configuration_json['plugins_config']['plugins']:
            _plugin = Plugin(
                plugin['name'],
                plugin['is_enabled']
            )

            plugins.append(_plugin)

        plugins_configuration = PluginsConfiguration(
            configuration_json['plugins_config']['will_load_all'],
            plugins
        )

        framework_configuration = FrameworkConfiguration(
            configuration_json['logs_directory'],
            configuration_json['mounting_point'],
            configuration_json['updates_intensity'],
            configuration_json['will_execute_builtin_tests'],
            configuration_json['testing_ports'],
            configuration_json['nuking_ports'],
            plugins_configuration
        )

        return framework_configuration

    def __read_configuration_file(self):
        try:
            with open(self._config_file_location, 'r') as configuration_file:
                configuration_json = configuration_file.read()
        except FileNotFoundError as file_not_found_error:
            print('>>> Configuration file was not found on it\'s default location.')
            print('>>> {}'.format(file_not_found_error))
