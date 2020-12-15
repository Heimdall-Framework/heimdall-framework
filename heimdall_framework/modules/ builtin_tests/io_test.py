import os
import shutil
from heimdall_framework.modules.data_provider import DataProvider
from heimdall_framework.modules.device_operations_provider import DeviceOperationsProvider 
from heimdall_framework.modules.system_operations_provider import SystemOperationsProvider
from heimdall_framework.modules.file_operations_provider import FileOperationsProvider


def run(logger, configuration, device, device_handle):
    DeviceOperationsProvider().handle_kernel_driver(device_handle, True)

    device_system_name = DeviceOperationsProvider().get_device_udev_property(device, 'DEVNAME')

    _, mounted_device_partition = SystemOperationsProvider().mount_device(configuration, logger, device_system_name)
    DataProvider().generate_random_data_file(logger)

    shutil.copyfile('dump.me', configuration.mounting_point  + 'dump.me')
    shutil.move(configuration.mounting_point  + 'dump.me', 'received_dump.me')
    
    if FileOperationsProvider().compare_files('dump.me', 'received_dump.me'):
        os.remove('dump.me')
        os.remove('received_dump.me')

        SystemOperationsProvider().unmount_device(logger, mounted_device_partition)
        DeviceOperationsProvider().handle_kernel_driver(device_handle, False)
        return True
    
    SystemOperationsProvider().unmount_device(logger, mounted_device_partition)        
    DeviceOperationsProvider().handle_kernel_driver(device_handle, False)

    os.remove('dump.me')
    os.remove('received_dump.me')
    
    return False