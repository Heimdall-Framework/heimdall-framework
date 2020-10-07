import os
import sys
import json
import shutil
import plugypy
import datetime 
import importlib
import usb1 as usb
from .logger import Logger
from .data_provider import DataProvider
from modules import gui_elements as gui
from .file_operations_provider import FileOperationsProvider
from .device_operations_provider import DeviceOperationsProvider
from .system_operations_provider import SystemOperationsProvider
from .network_operations_provider import NetworkOperationsProvider

TESTS_RANGE = 4

class Evaluator():

    def __init__(self, device_handle, port_number, context):
        self.device_mountpoint = os.environ['DEVS_MOUNTPOINT']
        self.__device = device_handle.getDevice()
        self.__device_handle = device_handle
        self.__port_number = port_number
        self.__context = context
        self.__plugins_directory = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../..', 'python/plugins'))
        self.__configuration_file_directory = self.__plugins_directory + '/config.json'
        
        Logger().log('>>> Evaluator was initialized.')

    def evaluate_device(self):
        Logger().log('>> Device testing initiated.')
        
        if not self.__validate_device_type():
            Logger().log('> Device type validation test failed.')
            return False, self.__device
        Logger().log('> Device type validation test was passed.')

        if not self.__validate_vendor_information():
            Logger().log('> Vendor validation test failed.')
            return False, self.__device
        Logger().log('> Vendor validation test was passed.')
    
        if not self.__virus_scan():
            Logger().log('> Virus scan failed.')
            return False, self.__device
        Logger().log('> Virus scan was passed.')

        if not self.__test_io():
            Logger().log('> IO test failed.')
            return False, self.__device
        Logger().log('> IO test was passed.')

        if not self.__intird_backdoor_test():
            Logger().log('> Initrd validation test failed.')
            return False, self.__device
        Logger().log('> Initrd validation test was passed.')       

        if not self.__run_external_tests():
            Logger().log('> External Test failed.')
            return False
        Logger().log('> All tests were successful.')

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
                gui.show_msg_box('Guideline', 'Unplug the USB device, click Okay and then plug it in tha same port.')

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

    def __validate_device_type(self):
        for device_configuration in self.__device.iterConfigurations():
            device_interface_class = next(device_configuration.__getitem__(0).__iter__()).getClass()
            
            self.__device_interface_class = device_interface_class
            if device_interface_class != 8 or device_configuration.getNumInterfaces() > 1:
                return False

            return True


    def __test_io (self):
        DeviceOperationsProvider().handle_kernel_driver(self.__device_handle, True)

        device_system_name = DeviceOperationsProvider().get_device_udev_property(self.__device, 'DEVNAME')

        _, mounted_device_partition = SystemOperationsProvider().mount_device(device_system_name)
        DataProvider().generate_random_data_file()

        shutil.copyfile('dump.me', self.device_mountpoint  + 'dump.me')
        shutil.move(self.device_mountpoint  + 'dump.me', 'received_dump.me')
        
        if FileOperationsProvider().compare_files('dump.me', 'received_dump.me'):
            os.remove('dump.me')
            os.remove('received_dump.me')

            SystemOperationsProvider().unmount_device(mounted_device_partition)
            DeviceOperationsProvider().handle_kernel_driver(self.__device_handle, False)
            return True
        
        SystemOperationsProvider().unmount_device(mounted_device_partition)        
        DeviceOperationsProvider().handle_kernel_driver(self.__device_handle, False)
    
        os.remove('dump.me')
        os.remove('received_dump.me')
        
        return False

    def __virus_scan(self):
        DeviceOperationsProvider().handle_kernel_driver(self.__device_handle, True)

        device_system_name = DeviceOperationsProvider().get_device_udev_property(self.__device, 'DEVNAME')
        _, mounted_device_partition = SystemOperationsProvider().mount_device(device_system_name)

        scan_result = DeviceOperationsProvider().virus_scan_device(self.device_mountpoint)
        SystemOperationsProvider().unmount_device(mounted_device_partition)
        DeviceOperationsProvider().handle_kernel_driver(self.__device_handle, False)

        return scan_result # bool

    def __intird_backdoor_test(self):
        DeviceOperationsProvider().handle_kernel_driver(self.__device_handle, True)

        device_system_name = DeviceOperationsProvider().get_device_udev_property(self.__device, 'DEVNAME')
        _, mounted_device_partition = SystemOperationsProvider().mount_device(device_system_name)
        
        indicator_file_path = FileOperationsProvider().find_file(self.device_mountpoint, 'tails.cfg')

        if indicator_file_path is None:
            Logger().log('> Indicator file does not exist in the filesystem. Test is being flaged as successful.')
            SystemOperationsProvider().unmount_device(mounted_device_partition)        

            return True
        else:
            Logger().log('> Packing live boot files into image file.')
            FileOperationsProvider().create_img_file('img')
            FileOperationsProvider().create_img_file('iso')

            Logger().log('> Generating image file checksum.')

            local_image_checksum = str(SystemOperationsProvider().get_file_checksum('/tmp/temp_image.img'))

            # compares the checksums from the Tails website to the local one
            if SystemOperationsProvider().offline_verify_checksum(local_image_checksum):
                os.remove('/tmp/temp_image.img')
                os.remove('/tmp/temp_image.iso')

                SystemOperationsProvider().unmount_device(mounted_device_partition)        
                return True
            else:
                os.remove('/tmp/temp_image.img')
                os.remove('/tmp/temp_image.iso')
                Logger().log('> The Tails image is outdated or has been altered. Please update your Tails liveboot to the newest version and test again.')
                
                SystemOperationsProvider().unmount_device(mounted_device_partition)                        
                return False

    # in development
    def __detect_time_targeted_payload(self):        
        current_time = datetime.datetime.now()
        new_system_time = datetime.datetime(2021, 1, 12, 13, 22, 13)

        # change the system time to a given one
        SystemOperationsProvider().change_system_time(new_system_time)
        
        # test stuff after the system time is changed 

        # return the system time to normal
        SystemOperationsProvider().change_system_time(new_system_time)

        print('Await further instructions')

    # set a device object with a given port
    def __set_device(self):
        while self.__device is None:
            self.__device = DeviceOperationsProvider().find_by_port_number(self.__port_number, self.__context)


    # set the device handle object of the currently connected device
    def __set_device_handle(self):
        while self.__device_handle is None:
            self.__device_handle = self.__context.openByVendorIDAndProductID(
                self.__device.getVendorID(),
                self.__device.getProductID()
            )

    # executes hardware relay controll plugin
    def __execute_hardware_plugin(self, delay):
        plugin_manager = plugypy.PluginManager(
            self.__plugins_directory,
            self.__configuration_file_directory,
            will_verify_ownership=True
            )

        hardware_controller_plugin = plugin_manager.import_plugin('hardware_controller')

        if hardware_controller_plugin == None:
            return False

        plugin_manager.execute_plugin(hardware_controller_plugin, (delay,), is_forced=True)
        return True
 
    # runs external plugins (tests)
    def __run_external_tests(self):
        plugin_arguments_tuple = (self.__device, self.__device_handle)

        plugin_manager = plugypy.PluginManager(
            self.__plugins_directory, 
            self.__configuration_file_directory, 
            will_verify_ownership=True
            )
        
        plugins_list = plugin_manager.import_plugins()

        for plugin in plugins_list:
            result = plugin_manager.execute_plugin(plugin, plugin_arguments_tuple)

            if result == False:
                print('Custom test: {} was not passed.'.format(plugin['name']))
                return False
        return True