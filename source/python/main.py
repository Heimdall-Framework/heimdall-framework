import usb1 as usb
import device_operations as dops
import analyser
import tests
from gui_elements import show_msg_box

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
                new_devices = dops.find_new_device(cached_devices, device_list)
                
                #caches the new devices
                cached_devices = device_list
                
                #lists the newly connected devices
                for device in new_devices:                                             
                    #initiates USB context for given device
                    with usb.USBContext() as context:
                        #creates a handler for a given USB context
                        handle = context.openByVendorIDAndProductID(device.getVendorID(), device.getProductID(), skip_on_error=True)

                        if handle is None:
                            print(">>> Device not present, or user is not allowed to use the device.")
                        else:
                            dops.handle_kernel_driver(handle)
                    
                        if device.getPortNumber() not in SERVICE_PORTS:
                            print(">>> Test device was connected. Initiating testing procedure...")

                            if tests.test_device(handle, device.getPortNumber(), context) != True:
                                print(">>>!!! DEVICE IS NOT SAFE !!!<<<")
                            else:
                                print(">>> Device is SAFE for use")
                        else:
                            dops.handle_kernel_driver(handle)
                            print(">>> Service device was connected.")
                                     
        else:
            cached_devices = device_list
            is_initiating = False