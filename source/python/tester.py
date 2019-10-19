import os
import shutil
import analyser
import usb1 as usb
import gui_elements as gui
from data_provider import DataProvider
from device_operations_provider import DeviceOperationsProvider
from logger import log

TESTS_RANGE = 4
DEVICE_MOUNTPOINT = '/home/ivan/mount_point/'
DUMPFILE_PATH = ''
class Tester:

    def __init__(self, device_handle, port_number, context):
        self.__device = device_handle.getDevice()
        self.__device_handle = device_handle
        self.__port_number = port_number
        self.__context = context

    def test_device(self):
        log('>> Device testing initiated.')

        if not self.__validate_vendor_information():
            log('> Test 0 failed.')
            return False
        log("> Test 0 was passed.")

        if not self.__validate_device_type():
            log("> Test 1 failed.")
            return False
        log("> Test 1 was passed.")
    
        self.__virus_scan()

        if not self.__test_io():
            log('> Test 2 failed.')
            return False
        log('> Test 2 was passed.')

        if not self.__intird_backdoor_test():
            log('> Test 3 failed.')
            return False
        log('> Test 3 was passed.')
        
        return True

    def __validate_vendor_information(self):
        device_vendor_id = self.__device.getVendorID()
        device_product_id = self.__device.getProductID()
        device_bcd_number = self.__device.getbcdDevice()

        self.__device = None
        self.__device_handle = None

        for i in range(TESTS_RANGE):
            #the following line will be removed as part of optimisation when suitable harware is present    
            gui.show_msg_box('Guidline', 'Unlpug the USB device, click Okay and then plug it in tha same port.')

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

        DeviceOperationsProvider().mount_device(device_system_name)
        DataProvider().generate_random_data_file()
        
        shutil.copyfile('dump.me', DEVICE_MOUNTPOINT  + 'dump.me')
        shutil.move(DEVICE_MOUNTPOINT  + 'dump.me', 'received_dump.me')

        if analyser.compare_files('dump.me', 'received_dump.me'):
            return True
        
        return False

    def __virus_scan(self):
        DeviceOperationsProvider().handle_kernel_driver(self.__device_handle, True)
       
        device_system_name = DeviceOperationsProvider().get_device_udev_property(self.__device, 'DEVNAME')
        
        DeviceOperationsProvider().mount_device(device_system_name)
        scan_result = DeviceOperationsProvider().virus_scan_device(DEVICE_MOUNTPOINT)
        
        DeviceOperationsProvider().handle_kernel_driver(self.__device_handle, False)

        return scan_result

    def __intird_backdoor_test(self):
        initrd_file_path = analyser.find_initrd(DEVICE_MOUNTPOINT)
        
        print(initrd_file_path)

        return True

    def __set_device(self):
        while self.__device is None:
            self.__device = DeviceOperationsProvider().find_by_port_number(self.__port_number, self.__context)


    def __set_device_handle(self):
        while self.__device_handle is None:
            self.__device_handle = self.__context.openByVendorIDAndProductID(
                self.__device.getVendorID(),
                self.__device.getProductID()
            )