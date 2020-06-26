import clamd
import subprocess
import pyudev as udev
import usb1 as usb
from logger import Logger

INTERFACE = 0
PORT_MARGIN = [0, 10]

class DeviceOperationsProvider():

    # finds new device on the bus
    def find_new_device(self, test_ports, nuke_ports, context): 
        # checks if a testabl device is present and returns it
        for test_port in test_ports:
            new_device = self.find_by_port_number(test_port, context) 
            if new_device !=None:
                return new_device
        
        # checks if a nukable device is present and returns is
        for nuke_port in nuke_ports:
            new_device = self.find_by_port_number(nuke_port, context) 
            if new_device !=None:
                return new_device

        # if no devices were found a NoneType object is returned
        return None

    def find_by_port_number(self, p_number, context):
        """
        Retrieves a device on a given port number and context

        :param p_number: The port number that is being checked for device
        :param context: usb1 context object
        """

        device_list = context.getDeviceList()
        for device in device_list:
            if device.getPortNumber() == p_number:
                return device

        return None
    
    def handle_kernel_driver(self, device_handle, driver_status):
        """
        Attaches or detaches the kernel driver for the device

        :param device_handle: The usb1 handle object of the device, whose kernel driver is being handled
        :param driver_status: The desired status of the kernel driver (attached or detached)
        """

        if driver_status:
           while not device_handle.kernelDriverActive(0):
               device_handle.attachKernelDriver(0)
        else:
            while device_handle.kernelDriverActive(0):
                device_handle.detachKernelDriver(0)

    def get_device_udev_property(self, device, udev_property):
        """
        Retrives an udev property for a given device

        :param device: The usb1 device object of the given device
        :param udev_property: The udev property that is being retrieved 
        """

        vid = device.getVendorID()
        pid = device.getProductID()

        context = udev.Context()

        devices_monitor = udev.Monitor.from_netlink(context)
        devices_monitor.filter_by('block')

        for action, dev in devices_monitor:
            if action != 'add':
                continue
            print(action)

            vid_hex = str(dev.get('ID_VENDOR_ID'))
            pid_hex = str(dev.get('ID_MODEL_ID'))
            
            if vid_hex != 'None' and pid_hex != 'None':
                if int(vid_hex, 16) == vid and int(pid_hex, 16) == pid:
                    target_property = dev.get(udev_property)
                    return target_property
                    
        return None
    
    def virus_scan_device(self, mountpoint_path):
        """
        Scans a device for viruses

        :param mountpoint_path: The path to the mountpoint directory of the connected device
        """
        
        clam_daemon = clamd.ClamdUnixSocket()
        clam_daemon.reload()

        Logger().log('> Initiating virus scan.')

        scan_result = clam_daemon.scan(mountpoint_path)
        Logger().log('> {}'.format(scan_result), silent=True)
        
        return 'OK' in str(scan_result)