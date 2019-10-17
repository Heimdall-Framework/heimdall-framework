import clamd
import subprocess
import psutil   
import pyudev as udev
import usb1 as usb
from logger import log
import pprint

INTERFACE = 0
class DeviceOperationsProvider:
    def find_new_device(self, old_device_list, new_device_list):    
        new_devices = []
        old_devices_ids_list = []

        for dev in old_device_list:
            old_devices_ids_list.append(dev.getProductID())

        for device in new_device_list:
            if device.getProductID() not in old_devices_ids_list:
                new_devices.append(device)

        return new_devices

    def find_by_port_number(self, p_number):
        with usb.USBContext() as context:
            device_list = context.getDeviceList()
            for device in device_list:
                if device.getPortNumber() == p_number:
                    return device

            return None

    def handle_kernel_driver(self, device_handle, driver_status):
        if driver_status:
           while not device_handle.kernelDriverActive(0):
               device_handle.attachKernelDriver(0)
        else:
            while device_handle.kernelDriverActive(0):
                device_handle.detachKernelDriver(0)

    def get_device_sys_name(self, device):
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
                    return dev.get('DEVNAME')
                    
        return None 
    
    def mount_device(self, mountpoint):
        mounting_command = 'sudo mount {0} /home/ivan/mount_point -o noexec'.format(mountpoint)

        process = subprocess.Popen(mounting_command.split(), stdout=subprocess.PIPE)

        output, error = process.communicate()

        if error != None:
            log(error)
            return False

        return True

    def virus_scan_device(self, mountpoint_path):
        clam_daemon = clamd.ClamdUnixSocket()
        clam_daemon.reload()

        log('> Initiating virus scan.')

        scan_result = clam_daemon.scan(mountpoint_path)
        
        print (scan_result)
