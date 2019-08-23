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
            if cached_devices is None or len(device_list) < len(cached_devices):
                cached_devices = device_list

            elif len(device_list) > len(cached_devices):
                new_devices = dops.find_new_device(cached_devices, device_list)
                cached_devices = device_list
                for device in new_devices:                    
                    if device.getPortNumber() not in SERVICE_PORTS:
                        print("Test device was connected. Initiating testing procedure...")
                        tests.test_device(device, device.getPortNumber())
                    else:
                        print("Service device was connected.")
                                     
        else:
            cached_devices = device_list
            is_initiating = False