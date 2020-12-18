import os
import sys
import json
import shutil
import datetime
import importlib
import usb1 as usb
from plugypy import *
from .logger import Logger
from .gui_provider import GuiProvider
from .data_provider import DataProvider
from .file_operations_provider import FileOperationsProvider
from .device_operations_provider import DeviceOperationsProvider
from .system_operations_provider import SystemOperationsProvider

TESTS_RANGE = 4


class Evaluator:
    def __init__(self, configuration, logger, device_handle, port_number, context):
        self.__configuration = configuration
        self.__plugins_config = configuration.plugins_config
        self.__logger = logger

        self.__device_mountpoint = configuration.mounting_point
        self.__device = device_handle.getDevice()
        self.__device_handle = device_handle
        self.__port_number = port_number
        self.__context = context

        self.__internals_plugins_directory = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "plugins")
        )
        self.__plugins_directory = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../", "plugins")
        )

        self.__logger.log(">>> Evaluator was initialized.")

    def evaluate_device(self) -> (bool, usb.USBDevice):
        """
        Evaluate device.
        """

        self.__logger.log(">> Device testing initiated.")

        tests = [self.__validate_device_type, self.__validate_vendor_information]

        for test in tests:
            if not test():
                self.__logger.log(">>> Test: {} FAILED.".format(test.__name__))
                return False, None

        return True, self.__device

    def __validate_vendor_information(self) -> bool:
        """
        Validate the vendor information of the tested device.
        """

        device_vendor_id = self.__device.getVendorID()
        device_product_id = self.__device.getProductID()
        device_bcd_number = self.__device.getbcdDevice()

        for _ in range(TESTS_RANGE):
            if not self.__execute_hardware_plugin(5):
                GuiProvider().show_msg_box(
                    "Guideline",
                    "Unplug the USB device, click Okay and then plug it in tha same port.",
                )

            self.__device = None
            self.__device_handle = None

            self.__set_device()
            self.__set_device_handle()

            DeviceOperationsProvider().handle_kernel_driver(self.__device_handle, False)

            test_vid = self.__device.getVendorID()
            test_pid = self.__device.getProductID()
            test_bcdn = self.__device.getbcdDevice()

            if (
                test_vid != device_vendor_id
                or test_pid != device_product_id
                or test_bcdn != device_bcd_number
            ):
                return False

        return True

    def __validate_device_type(self) -> bool:
        for device_configuration in self.__device.iterConfigurations():
            device_interface_class = next(
                device_configuration.__getitem__(0).__iter__()
            ).getClass()

            self.__device_interface_class = device_interface_class
            if (
                device_interface_class != 8
                or device_configuration.getNumInterfaces() > 1
            ):
                return False

            return True

    def __set_device(self) -> None:
        while self.__device is None:
            self.__device = DeviceOperationsProvider().find_by_port_number(
                self.__port_number, self.__context
            )

    # Set the device handle object of the currently connected device.
    def __set_device_handle(self) -> None:
        while self.__device_handle is None:
            self.__device_handle = self.__context.openByVendorIDAndProductID(
                self.__device.getVendorID(), self.__device.getProductID()
            )

    def __execute_hardware_plugin(self, delay) -> bool:
        if SystemOperationsProvider(4).is_running_on_pi():
            # Only import the hardware plugin if the device is RPI-based and has GPIO pins
            from .gpio_operations_provider import GPIOOperationsProvider

            GPIOOperationsProvider().trigger_relay_restart(1)

    def __run_builtin(self) -> bool:
        configuration_deserializer = ConfigurationDeserializer(
            "builtin_tests/builtin_config.json"
        )
        builtins_configuration = configuration_deserializer.deserialize_config()

        plugin_manager = PluginManager("builtin_tests", builtins_configuration)

        discovered_plugins = plugin_manager.discover_plugins()
        imported_plugins = plugin_manager.import_plugins(discovered_plugins)

        builtin_tests_arguments = (
            self.__logger,
            self.__configuration,
            self.__device,
            self.__device_handle,
        )

        for plugin in imported_plugins:
            test_result = plugin_manager.execute_plugin_function(
                plugin, "run", builtin_tests_arguments
            )

            if not test_result:
                return False
        return True

    def __run_external_tests(self) -> bool:
        plugin_manager = PluginManager(
            self.__configuration.plugins_folder_location, self.__plugins_config
        )

        discovered_plugins = plugin_manager.discover_plugins()
        imported_plugins = plugin_manager.import_plugins(discovered_plugins)

        builtin_tests_arguments = (
            self.__logger,
            self.__configuration,
            self.__device,
            self.__device_handle,
        )

        for plugin in imported_plugins:
            test_result = plugin_manager.execute_plugin_function(
                plugin, "run", builtin_tests_arguments
            )

            if not test_result:
                return False
        return True
