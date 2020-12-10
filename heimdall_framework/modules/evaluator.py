import os
import sys
import json
import shutil
import plugypy
import datetime 
import importlib
import usb1 as usb
from .logger import Logger
from .gui_provider import GuiProvider
from .data_provider import DataProvider
from .file_operations_provider import FileOperationsProvider
from .device_operations_provider import DeviceOperationsProvider
from .system_operations_provider import SystemOperationsProvider

TESTS_RANGE = 4

class Evaluator():

    def __init__(self, configuration, logger, device_handle, port_number, context):
        self.__configuration = configuration
        self.__plugins_config= configuration.plugins_config
        self.__logger = logger
        
        self.__device_mountpoint = configuration.mounting_point
        self.__device = device_handle.getDevice()
        self.__device_handle = device_handle
        self.__port_number = port_number
        self.__context = context

        self.__plugins_directory = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../', 'plugins'))
        
        self.__load_plugins()
        self.__logger.log('>>> Evaluator was initialized.')

    def evaluate_device(self) -> (bool, usb.USBDevice):
        """
        Evaluate device.
        """ 

        self.__logger.log('>> Device testing initiated.')
        
        tests = [
            self.__validate_device_type,
            self.__validate_vendor_information,
            self.__virus_scan,
            self.__test_io,
            self.__intird_backdoor_test
            #self.__run_external_tests
        ]

        for test in tests:
            if not test():
                self.__logger.log('>>> Test: {} FAILED.'.format(test.__name__))
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
                GuiProvider().show_msg_box('Guideline', 'Unplug the USB device, click Okay and then plug it in tha same port.')

            self.__device = None
            self.__device_handle = None

            self.__set_device()
            self.__set_device_handle()

            DeviceOperationsProvider().handle_kernel_driver(self.__device_handle, False)

            test_vid = self.__device.getVendorID()
            test_pid = self.__device.getProductID()
            test_bcdn = self.__device.getbcdDevice()
            
            if test_vid != device_vendor_id or test_pid != device_product_id or test_bcdn != device_bcd_number:
                return False
        
        return True

    def __validate_device_type(self) -> bool:
        for device_configuration in self.__device.iterConfigurations():
            device_interface_class = next(device_configuration.__getitem__(0).__iter__()).getClass()
            
            self.__device_interface_class = device_interface_class
            if device_interface_class != 8 or device_configuration.getNumInterfaces() > 1:
                return False

            return True


    def __test_io (self) -> bool:
        DeviceOperationsProvider().handle_kernel_driver(self.__device_handle, True)

        device_system_name = DeviceOperationsProvider().get_device_udev_property(self.__device, 'DEVNAME')

        _, mounted_device_partition = SystemOperationsProvider().mount_device(self.__configuration, self.__logger, device_system_name)
        DataProvider().generate_random_data_file(self.__logger)

        shutil.copyfile('dump.me', self.__device_mountpoint  + 'dump.me')
        shutil.move(self.__device_mountpoint  + 'dump.me', 'received_dump.me')
        
        if FileOperationsProvider().compare_files('dump.me', 'received_dump.me'):
            os.remove('dump.me')
            os.remove('received_dump.me')

            SystemOperationsProvider().unmount_device(self.__logger, mounted_device_partition)
            DeviceOperationsProvider().handle_kernel_driver(self.__device_handle, False)
            return True
        
        SystemOperationsProvider().unmount_device(self.__logger, mounted_device_partition)        
        DeviceOperationsProvider().handle_kernel_driver(self.__device_handle, False)
    
        os.remove('dump.me')
        os.remove('received_dump.me')
        
        return False

    def __virus_scan(self) -> bool:
        """
        Scan tested device for viruses.
        """
        DeviceOperationsProvider().handle_kernel_driver(self.__device_handle, True)

        device_system_name = DeviceOperationsProvider().get_device_udev_property(self.__device, 'DEVNAME')
        _, mounted_device_partition = SystemOperationsProvider().mount_device(self.__configuration, self.__logger, device_system_name)

        scan_result = DeviceOperationsProvider().virus_scan_device(self.__device_mountpoint)
        SystemOperationsProvider().unmount_device(self.__logger, mounted_device_partition)
        DeviceOperationsProvider().handle_kernel_driver(self.__device_handle, False)

        return scan_result

    def __intird_backdoor_test(self) -> bool:
        DeviceOperationsProvider().handle_kernel_driver(self.__device_handle, True)

        device_system_name = DeviceOperationsProvider().get_device_udev_property(self.__device, 'DEVNAME')
        _, mounted_device_partition = SystemOperationsProvider().mount_device(self.__configuration, self.__logger, device_system_name)
        
        indicator_file_path = FileOperationsProvider().find_file(self.__device_mountpoint, 'tails.cfg')

        if indicator_file_path is None:
            self.__logger.log('> Indicator file does not exist in the filesystem. Test is being flaged as successful.')
            SystemOperationsProvider().unmount_device(self.__logger, mounted_device_partition)        

            return True
        else:
            self.__logger.log('> Packing live boot files into image file.')
            FileOperationsProvider().create_img_file(self.__logger, 'img')
            FileOperationsProvider().create_img_file(self.__logger, 'iso')

            self.__logger.log('> Generating image file checksum.')

            local_image_checksum = str(SystemOperationsProvider().get_file_checksum(self.__logger, '/tmp/temp_image.img'))

            # compares the checksums from the Tails website to the local one
            if SystemOperationsProvider().offline_verify_checksum(local_image_checksum):
                os.remove('/tmp/temp_image.img')
                os.remove('/tmp/temp_image.iso')

                SystemOperationsProvider().unmount_device(self.__logger, mounted_device_partition)        
                return True
            else:
                os.remove('/tmp/temp_image.img')
                os.remove('/tmp/temp_image.iso')
                self.__logger.log('> The Tails image is outdated or has been altered. Please update your Tails liveboot to the newest version and test again.')
                
                SystemOperationsProvider().unmount_device(self.__logger, mounted_device_partition)                        
                return False

    def __set_device(self) -> None:
        while self.__device is None:
            self.__device = DeviceOperationsProvider().find_by_port_number(self.__port_number, self.__context)


    # set the device handle object of the currently connected device
    def __set_device_handle(self) -> None:
        while self.__device_handle is None:
            self.__device_handle = self.__context.openByVendorIDAndProductID(
                self.__device.getVendorID(),
                self.__device.getProductID()
            )

    # executes hardware relay controll plugin
    def __execute_hardware_plugin(self, delay) -> bool:
        for plugin in self.__imported_plugins:
            if plugin.name == 'hardware_controller':
                self.__logger.log('Hardware controller was found.')
                self.__plugin_manager.execute_plugin_function(plugin, 'toggle', (delay,))
 

    def __run_testing_plugins(self) -> bool:
        pass
    # runs external plugins (tests)
    # def __run_external_tests(self) -> bool:
    #     plugin_arguments_tuple = (self.__device, self.__device_handle)

    #     plugin_manager = plugypy.PluginManager(
    #         self.__plugins_directory, 
    #         self.__plugins_config, 
    #         will_verify_ownership=True
    #         )
        
    #     plugins_list = plugin_manager.import_plugins()

    #     for plugin in plugins_list:
    #         result = plugin_manager.execute_plugin(plugin, plugin_arguments_tuple)

    #         if result == False:
    #             print('Custom test: {} was not passed.'.format(plugin['name']))
    #             return False
    #     return True

    def __load_plugins(self):
        plugin_manager = plugypy.PluginManager(
            self.__plugins_directory,
            self.__plugins_config,
            will_verify_ownership=True
        )

        discovered_pluggins = plugin_manager.discover_plugins()
        imported_plugins = plugin_manager.import_plugins(discovered_pluggins)

        self.__plugin_manager = plugin_manager
        self.__imported_plugins = imported_plugins
