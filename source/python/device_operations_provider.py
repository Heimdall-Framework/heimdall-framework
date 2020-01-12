import clamd
import subprocess
import psutil
import pyudev as udev
import usb1 as usb
from logger import log

INTERFACE = 0

class DeviceOperationsProvider():

    # finds new device on the bus
    def find_new_device(self, test_ports, context):    
        new_device = None

        while new_device == None:
            for test_port in test_ports:
                new_device = self.find_by_port_number(test_port, context) 
                
                if new_device != None:
                    return new_device

    # finds a device for a given port number and context
    def find_by_port_number(self, p_number, context):
        device_list = context.getDeviceList()
        for device in device_list:
            if device.getPortNumber() == p_number:
                return device

        return None
    
    # attaches or detaches the kernel driver for the device
    def handle_kernel_driver(self, device_handle, driver_status):
        if driver_status:
           while not device_handle.kernelDriverActive(0):
               device_handle.attachKernelDriver(0)
        else:
            while device_handle.kernelDriverActive(0):
                device_handle.detachKernelDriver(0)

    # gets an udev property for a given device
    def get_device_udev_property(self, device, udev_property):
        vid = device.getVendorID()
        pid = device.getProductID()

        context = udev.Context()

        devices_monitor = udev.Monitor.from_netlink(context)
        devices_monitor.filter_by('block')

        for action, dev in devices_monitor:
            vid_hex = str(dev.get('ID_VENDOR_ID'))
            pid_hex = str(dev.get('ID_MODEL_ID'))
            
            if vid_hex != 'None' and pid_hex != 'None':
                if int(vid_hex, 16) == vid and int(pid_hex, 16) == pid:
                    target_property = dev.get(udev_property)
                    return target_property 
                    
        return None
    
    # scnas a device for viruses
    def virus_scan_device(self, mountpoint_path):
        clam_daemon = clamd.ClamdUnixSocket()
        clam_daemon.reload()

        log('> Initiating virus scan.')

        scan_result = clam_daemon.scan(mountpoint_path)

        if 'OK' in str(scan_result):
            return True
        else:
            return False