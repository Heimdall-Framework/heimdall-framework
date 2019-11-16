import usb1 as usb
from logger import log
from evaluator import Evaluator
from device_operations_provider import DeviceOperationsProvider

SERVICE_PORTS = [0,2]

class USBHotplugDetector():
    def __init__(self):
        self.__is_initiating = True
        self.__cached_devices = []
        
    def start(self):
        self.__is_started = True
        self.__begin_detecting()
        
    def stop(self):
        self.__is_started = False

    def __begin_detecting(self):
        while self.__is_started:
            with usb.USBContext() as context:
                device_list = context.getDeviceList()
                
                if not self.__is_initiating:
                    # if cached devices count is less than the real count of conencted devices
                    if cached_devices is None or len(device_list) < len(cached_devices):
                        #caches the currently currently connected devices in a collection
                        cached_devices = device_list

                    # if real count of connected devices is more tha the count of the cached ones
                    elif len(device_list) > len(cached_devices):
                        # creates a list that contains only the newly connected devices
                        new_devices = DeviceOperationsProvider().find_new_device(
                            cached_devices,
                            device_list
                            )
                        
                        # caches the new devices
                        cached_devices = device_list
                        
                        # lists the newly connected devices
                        for device in new_devices:                                             
                            # creates a handler for a given USB context
                            handle = context.openByVendorIDAndProductID(
                                device.getVendorID(), 
                                device.getProductID(), 
                                skip_on_error=True
                                )

                            if handle is None:
                                log(">>> Device not present, or user is not allowed to use the device.")
                            else:
                                DeviceOperationsProvider().handle_kernel_driver(handle, False)
                                
                                if device.getPortNumber() not in SERVICE_PORTS:
                                    log(">>> Test device was connected. Initiating testing procedure...")

                                    tester = Evaluator(
                                        handle, 
                                        device.getPortNumber(), 
                                        context
                                        )
                                    print(device.getPortNumber())
                                    if not tester.test_device():
                                        log(">>>!!! DEVICE IS NOT SAFE !!!<<<")
                                        
                                        handle.close()
                                        tester = None
                                    else:
                                        log(">>> Device is SAFE for use")
                                        
                                        handle.close()
                                        tester = None
                                else:
                                    DeviceOperationsProvider().handle_kernel_driver(handle, True)
                                    log(">>> Service device was connected.")                          
                else:
                    cached_devices = device_list
                    self.__is_initiating = False
        print('>>> Detector was terminated.')