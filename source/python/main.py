import usb1 as usb
import device_operations as dops
import analyser
from device_operations import DeviceOperationsProvider
from tester import Tester
from gui_elements import show_msg_box
from logger import log

SERVICE_PORTS = [0,2]
UNPLUGGING_TESTS_COUNT = 4

is_initiating = True
cached_devices = []

while True:
    with usb.USBContext() as context:
        device_list = context.getDeviceList()
        
        if not is_initiating:
            #if cached devices count is less than the real count of conencted devices
            if cached_devices is None or len(device_list) < len(cached_devices):
                #caches the currently currently connected devices in a collection
                cached_devices = device_list

            #if real count of connected devices is more tha the count of the cached ones
            elif len(device_list) > len(cached_devices):
                #creates a list that contains only the newly connected devices
                new_devices = DeviceOperationsProvider().find_new_device(
                    cached_devices,
                    device_list
                    )
                
                #caches the new devices
                cached_devices = device_list
                
                #lists the newly connected devices
                for device in new_devices:                                             
                    #creates a handler for a given USB context
                    handle = context.openByVendorIDAndProductID(
                        device.getVendorID(), 
                        device.getProductID(), 
                        skip_on_error=True
                        )

                    if handle is None:
                        log(">>> Device not present, or user is not allowed to use the device.")
                    else:
                        DeviceOperationsProvider().handle_kernel_driver(handle)
                    
                    if device.getPortNumber() not in SERVICE_PORTS:
                        log(">>> Test device was connected. Initiating testing procedure...")
                        
                        tester = Tester(
                            handle, 
                            device.getPortNumber(), 
                            context
                            )

                        if tester.test_device() != True:
                            log(">>>!!! DEVICE IS NOT SAFE !!!<<<")
                        else:
                            log(">>> Device is SAFE for use")
                    else:
                        DeviceOperationsProvider().handle_kernel_driver(handle)
                        log(">>> Service device was connected.")
                                     
        else:
            cached_devices = device_list
            is_initiating = False