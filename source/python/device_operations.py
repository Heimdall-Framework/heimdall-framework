import usb1 as usb

INTERFACE = 0

def find_new_device(old_device_list, new_device_list):    
    new_devices = []
    old_devices_ids_list = []

    for dev in old_device_list:
        old_devices_ids_list.append(dev.getProductID())

    for device in new_device_list:
        if device.getProductID() not in old_devices_ids_list:
            new_devices.append(device)

    return new_devices

def find_by_port_number(p_number):
    with usb.USBContext() as context:
        device_list = context.getDeviceList()
        for device in device_list:
            if device.getPortNumber() == p_number:
                return device
        return None

def handle_kernel_driver(device_handle):
    if device_handle.kernelDriverActive(0):
        device_handle.detachKernelDriver(0)
    else:
        device_handle.attachKernelDriver(0)