import os
import data_provider
import usb1 as usb
import gui_elements as gui
import device_operations as dops
from logger import log

TESTS_RANGE = 4

class Tester:

    def __init__(self, device_handle, port_number, context):
        self.__device = device_handle.getDevice()
        self.__device_handle = device_handle
        self.__port_number = port_number
        self.__context = context

    def test_device(self):
        log('>> Device testing initiated.')

        if self.__unplugging_test() == False:
            log("> Test 0 failed.")
            return False
        log("> Test 0 was passed.")
        
        if self.__detect_device_type_test() == False:
            log("> Test 1 failed.")
            return False
        log("> Test 1 was passed.")
        

        return True

    def __unplugging_test(self):
        device_vendor_id = self.__device.getVendorID()
        device_product_id = self.__device.getProductID()
        device_bcd_number = self.__device.getbcdDevice()

        for i in range(TESTS_RANGE):
            #the following line will be removed as part of optimisation when suitable harware is present    
            gui.show_msg_box('Guidline', 'Unlpug the USB device, click Okay and then plug it in tha same port.')
            
            # the following two lines will be optimised when suitable hardware is present
            while dops.find_by_port_number(self.__port_number) is None:
                a = 0 #empty operation        

            self.__device = dops.find_by_port_number(self.__port_number)

            self.__device_handle = None

            self.__context.openByVendorIDAndProductID(
                self.__device.getVendorID(),
                self.__device.getProductID()
            )

            test_vid = self.__device.getVendorID()
            test_pid = self.__device.getProductID()
            test_bcdn = self.__device.getbcdDevice()

            if test_vid != device_vendor_id or test_pid != device_product_id or test_bcdn != device_bcd_number:
                return False

        return True

    def __detect_device_type_test(self):
        for device_configuration in self.__device.iterConfigurations():
            device_interface_class = next(device_configuration.__getitem__(0).__iter__()).getClass()
            
            self.__device_interface_class = device_interface_class

            #bug, fix it!
            if device_interface_class != 8 or device_configuration.getNumInterfaces() > 1:
                return False
            return True

        #unused function
    def __io_lightweight_testing(self):
        return None