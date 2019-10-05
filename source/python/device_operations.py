import clamd
import subprocess
import usb1 as usb

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

    def handle_kernel_driver(self, device_handle):
        if device_handle.kernelDriverActive(0):
            device_handle.detachKernelDriver(0)
        else:
            device_handle.attachKernelDriver(0)

    def get_mount_point(self, device_handle):
        serial_number = device_handle.getSerialNumber()
        command = 'sudo lsblk'
        grep = 'grep a'
        
        finder_process = subprocess.Popen(
            command.split(),
            stdout=subprocess.PIPE
            )
        
        
        grepper_process = subprocess.Popen(
            grep.split(),
            stdin=finder_process.stdout,
            stdout = subprocess.PIPE,
            stderr=subprocess.PIPE
            )

        finder_process.stdout.close()

        result, error = grepper_process.communicate()

        if error != '' or error != None:
            return None 
    
    def virus_scan_device(self, mountpoint_path):
        clam_daemon = clamd.ClamdUnixSocket()
        clam_daemon.reload()

        scan_result = clam_daemon.scan(mountpoint_path)

        print (scan_result)


