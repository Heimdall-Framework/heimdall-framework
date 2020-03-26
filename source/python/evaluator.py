import os
import sys
import json
import shutil
import importlib
import plugins
import usb1 as usb
import gui_elements as gui
from logger import Logger
from data_provider import DataProvider
from file_operations_provider import FileOperationsProvider
from device_operations_provider import DeviceOperationsProvider
from system_operations_provider import SystemOperationsProvider
from network_operations_provider import NetworkOperationsProvider

TESTS_RANGE = 4

class Evaluator():

    def __init__(self, device_handle, port_number, context):
        self.device_mountpoint = os.environ['DEVS_MOUNTPOINT']
        self.__device = device_handle.getDevice()
        self.__device_handle = device_handle
        self.__port_number = port_number
        self.__context = context
        self.__load_external_tests_config()

        Logger().log('>>> Evaluator was initialized.')
    def __load_external_tests_config(self):
        with open(os.path.join(sys.path[0], 'config.json')) as config_file:
            self.__plugins_config = json.load(config_file)

    def test_device(self):
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

    def __validate_vendor_information(self):
        device_vendor_id = self.__device.getVendorID()
        device_product_id = self.__device.getProductID()
        device_bcd_number = self.__device.getbcdDevice()

        for i in range(TESTS_RANGE):
            #the following line will be removed as part of optimisation when suitable harware is present    
            gui.show_msg_box('Guidline', 'Unlpug the USB device, click Okay and then plug it in tha same port.')

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

        SystemOperationsProvider().mount_device(device_system_name)
        DataProvider().generate_random_data_file()
        
        shutil.copyfile('dump.me', self.device_mountpoint  + 'dump.me')
        shutil.move(self.device_mountpoint  + 'dump.me', 'received_dump.me')
        if FileOperationsProvider().compare_files('dump.me', 'received_dump.me'):
            os.remove('dump.me')
            os.remove('received_dump.me')

            DeviceOperationsProvider().handle_kernel_driver(self.__device_handle, False)
            return True
        
        DeviceOperationsProvider().handle_kernel_driver(self.__device_handle, False)
    
        os.remove('dump.me')
        os.remove('received_dump.me')
        
        return False

    def __virus_scan(self):
        DeviceOperationsProvider().handle_kernel_driver(self.__device_handle, True)

        device_system_name = DeviceOperationsProvider().get_device_udev_property(self.__device, 'DEVNAME')
        SystemOperationsProvider().mount_device(device_system_name)
        
        scan_result = DeviceOperationsProvider().virus_scan_device(self.device_mountpoint)
        DeviceOperationsProvider().handle_kernel_driver(self.__device_handle, False)

        return scan_result # bool

    def __intird_backdoor_test(self):
        DeviceOperationsProvider().handle_kernel_driver(self.__device_handle, True)

        device_system_name = DeviceOperationsProvider().get_device_udev_property(self.__device, 'DEVNAME')
        SystemOperationsProvider().mount_device(device_system_name)

        initrd_file_path = FileOperationsProvider().find_initrd(self.device_mountpoint)
        
        if initrd_file_path is None:
            Logger().log('> Initrd file does not exist in the filesystem. Test is being flaged as successful.')
            return True
        else:
            Logger().log('> Packing live boot files into image file.')
            FileOperationsProvider().create_img_file()

            Logger().log('> Generating initrd file checksum.')

            local_image_checksum = SystemOperationsProvider().get_file_checksum('/tmp/temp_image.img')
            real_checksum = NetworkOperationsProvider().get_tails_checksum()
            
            if real_checksum is None:
                Logger().log('> Exception occured. The most common problem is lack of initernet connection or broken network driver.')
                Logger().log('> Trying hash verification from offline blacklist.')

                return SystemOperationsProvider().offline_verify_checksum(local_image_checksum)

            if local_image_checksum == real_checksum:
                os.remove('/tmp/temp_image.img')
                return True
            else:
                os.remove('/tmp/temp_image.img')
                return False

    def __detect_time_targeted_payload(self):
        print('Await further instructions')

    def __set_device(self):
        while self.__device is None:
            self.__device = DeviceOperationsProvider().find_by_port_number(self.__port_number, self.__context)


    def __set_device_handle(self):
        while self.__device_handle is None:
            self.__device_handle = self.__context.openByVendorIDAndProductID(
                self.__device.getVendorID(),
                self.__device.getProductID()
            )

    def __run_external_tests(self):
        for plugin in dir(plugins):
            item = getattr(plugins, plugin)

            plugin_location = '{}/plugins/{}.py'.format(
                os.path.dirname(os.path.realpath(__file__)),
                plugin
            )
            
            if os.path.exists(plugin_location):
                if not SystemOperationsProvider().verify_file_owner(plugin_location):
                    Logger().log('> Plugin {} does not belong to the user. It execution is being skipped because it might be malicious.'.format(
                        plugin
                    ))
                    continue
                
            if callable(item) and self.__validate_plugin(plugin):
                if not item(self.__device, self.__device_handle):
                    Logger().log('> External test {} failed or is not valid.'.format(item))
                    return False
        return True
    
    # validates if a given demo test exist in the config.json file and if it is allowed to be executed
    def __validate_plugin(self, plugin_name):
        for plugin_configuration in self.__plugins_config:
            if plugin_configuration['name'] == plugin_name and plugin_configuration['enabled']:
                return True
        return False
