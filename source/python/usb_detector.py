import os
import usb1 as usb
import gui_elements
from nuker import Nuker
from logger import Logger
from evaluator import Evaluator
from device_operations_provider import DeviceOperationsProvider


class USBHotplugDetector():
    def __init__(self):
        self.__cached_device = None
        self.__testing_ports = [int(port_number) for port_number in os.environ['TESTING_PORTS'].split(',')]
        self.__nuking_ports = [int(port_number) for port_number in os.environ['NUKING_PORTS'].split(',')]
        self.__cached_nuked_device = None
        self.__cached_tested_device = None

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
                    device = DeviceOperationsProvider().find_new_device(self.__testing_ports, self.__nuking_ports, context)

                    # checks if the found device has already been tested
                    if device is None or device == self.__cached_tested_device or device == self.__cached_nuked_device:
                        continue

                    # creates USBDeviceHandle object for given VID and PID
                    handle = context.openByVendorIDAndProductID(
                        device.getVendorID(),
                        device.getProductID(),
                        skip_on_error=True
                    )

                    # checks if the device is still present ot if the user is allowed to access it
                    if handle is None:
                        Logger().log(">>> Device not present or user is not allowed to use the device.")
                    else:
                        if device.getPortNumber() in self.__nuking_ports:
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
                            #self.__cache_nuked_device(None)
                        handle.close()

                Logger().log(">>> Hotplug detector was terminated.")
                
        except usb.USBError:
            Logger().log('>>> An exception has occurred')
        
    def __evaluate_device(self, device, handle, context):
        # detaches device's kernel driver
        DeviceOperationsProvider().handle_kernel_driver(handle, False)

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

    def __cache_tested_device(self, device):
        self.__cached_tested_device = device
    def __cache_nuked_device(self, device):
        self.__cached_nuked_device = device