import pyudev

ALREADY_CONNECTED_DEVICE_NODE = 'None'


def is_being_plugged(device):
    if device.action == "add":
        return True
    else:
        return False

context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem='usb')


while True:
    for device in iter(monitor.poll, None):
        if is_being_plugged(device):
            if str(device.device_node) != ALREADY_CONNECTED_DEVICE_NODE:
                print('A USB device with the following information was connected:')
                print('Vendor ID: %s' %device.get('ID_VENDOR_FROM_DATABASE'))
                print('Product model: %s' %device.get('ID_MODEL'))
                print('Product type: %s' %device.get('DEVTYPE'))
                print('Main partition label: %s' %device.get('ID_FS_LABEL'))
                print('Usage: %s' %device.get('ID_FS_USAGE'))
                