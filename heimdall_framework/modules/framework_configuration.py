from typing import List
from plugypy import Configuration as PluginsConfiguration


class FrameworkConfiguration(object):
    logs_directory: str
    mounting_point: str
    updates_intensity: str
    will_execute_builtin_tests: bool
    testing_ports: List[int]
    nuking_ports: List[int]
    plugins_config: PluginsConfiguration

    def __init__(self, logs_directory: str, mounting_point: str, updates_intensity: str, will_execute_builtin_tests: str, testing_ports: List[int], nuking_ports: List[int], plugins_config: PluginsConfiguration):
        self.logs_directory = logs_directory
        self.mounting_point = mounting_point
        self.updates_intensity = updates_intensity
        self.testing_ports = testing_ports
        self.nuking_ports = nuking_ports
        self.plugins_config = plugins_config
        self.will_execute_builtin_tests = will_execute_builtin_tests

    def __str__(self):
        framework_string = 'Framework Configuration: \n'
        framework_string += '\tLogs Directory: {}\n'.format(
            self.logs_directory)
        framework_string += '\tMounting Point: {}\n'.format(
            self.mounting_point)
        framework_string += '\tUpdates Intensity: {}\n'.format(
            self.updates_intensity)
        framework_string += '\tWill Execute Builtin Tests: {}\n'.format(
            self.will_execute_builtin_tests)
        framework_string += '\tTesting Ports: {}\n'.format(
            self.testing_ports)
        framework_string += '\tNuking Ports: {}\n'.format(
            self.nuking_ports)
        framework_string += '\tPlugins Configuration: {}\n'.format(
            str(self.plugins_config))

        return framework_string
