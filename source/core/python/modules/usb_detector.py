import os
import usb1 as usb
from .nuker import Nuker
from .logger import Logger
from .evaluator import Evaluator
from modules import gui_elements as gui_elements
from .device_operations_provider import DeviceOperationsProvider


class USBHotplugDetector():
    def __init__(self, configuration):
        self.__configuration = configuration
        self.__testing_ports = configuration.testing_ports
        self.__nuking_ports = configuration.nuking_ports
        self.__cached_device = None
        self.__nuked_device = None
        self.__tested_device = None

    def start(self):
        self.__is_started = True
        self.__begin_detecting()

    def stop(self):
        self.__is_started = False
        print('>>> Hotplug detector was stopped.')

    def __begin_detecting(self):
        Logger().log(">>> Hotplug detector was started.")
        
        try:
            with usb.USBContext() as context:
                while self.__is_started:
                    # finds a new device that can be tested
                    device = DeviceOperationsProvider().find_new_device(
                        self.__testing_ports, 
                        self.__nuking_ports, context
                        )

                    # checks if the found device has already been tested
                    if device is None or device == self.__tested_device or device == self.__nuked_device:
                        continue

                    # creates USBDeviceHandle object for given VID and PID
                    handle = context.openByVendorIDAndProductID(
                        device.getVendorID(),
                        device.getProductID(),
                        skip_on_error=True
                    )
                    
                    DeviceOperationsProvider().handle_kernel_driver(handle, False)
                    
                    # checks if the device is still present ot if the user is allowed to access it
                    if handle is None:
                        Logger().log(">>> Device not present or user is not allowed to use the device.")
                    else:
                        if device.getPortNumber() in self.__nuking_ports:
                            if gui_elements.show_confirm_box('Nuking Alert', 'You will not be able to recover the data from the nuked device. \nDo you want to proceed?'):
                                self.__nuke_device(device)
                        elif device.getPortNumber() in self.__testing_ports:
                            evaluation_result, evaluated_device = self.__evaluate_device(
                                device,
                                handle,
                                context
                            )

                            # indicates that the tested device is NOT safe for use
                            if not evaluation_result:
                                Logger().log(">>>! DEVICE IS NOT SAFE !<<<")
                                gui_elements.show_msg_box('Dangerous device detected','The tested device is NOT safe for use.') 
                           
                            # indicates that the tested device is safe for use
                            else:                                
                                Logger().log(">>> Device is SAFE for use")
                                gui_elements.show_msg_box('Passed','All tests were passed. The tested device is safe for use.')
                            
                            self.__cache_tested_device(evaluated_device)
                        handle.close()

                Logger().log(">>> Hotplug detector was terminated.")
                
        except usb.USBError:
            Logger().log('>>> An exception has occurred')
        
    def __evaluate_device(self, device, handle, context):
        # creates Evaluator object with given USBDeviceHandlem, USBDevice and device's USBContext
        evaluator = Evaluator(
            handle,
            device.getPortNumber(),
            context
            )

        result, returned_device = evaluator.evaluate_device()

        evaluator = None
        return result, returned_device

    def __nuke_device(self, device):
        device_partition = DeviceOperationsProvider().get_device_udev_property(device, 'DEVNAME')
        nuker = Nuker(device_partition)
                            
        Logger().log('>> Nuking device on port: {}'.format(device.getPortNumber()))
        Logger().log('>> Hang tight, it will take some time.')
        nuker.nuke()
        Logger().log('>>> Nuking finished.')
                            
        # cacheing fake device in order to allow testing for the same device immediately after nuking 
        self.__cache_nuked_device(device)
        self.__cache_tested_device(None)

    # caches the device that was just tested
    def __cache_tested_device(self, device):
        self.__tested_device = device

    # caches the device that was just nuked
    def __cache_nuked_device(self, device):
        self.__nuked_device = device