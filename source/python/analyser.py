import pyudev

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
            print('Device with vendor ID {} and product ID UNKNOWN was plugged.'.format(device.get('ID_VENDOR_FROM_DATABASE'), ))