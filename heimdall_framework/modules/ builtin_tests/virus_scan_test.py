import os
import shutil
from heimdall_framework.modules.data_provider import DataProvider
from heimdall_framework.modules.device_operations_provider import DeviceOperationsProvider
from heimdall_framework.modules.system_operations_provider import SystemOperationsProvider
from heimdall_framework.modules.file_operations_provider import FileOperationsProvider


def run(logger, configuration, device, device_handle):
    """
    Scan tested device for viruses.
    """
    DeviceOperationsProvider().handle_kernel_driver(device_handle, True)

    device_system_name = DeviceOperationsProvider().get_device_udev_property(
        device, "DEVNAME"
    )
    _, mounted_device_partition = SystemOperationsProvider().mount_device(
        configuration, logger, device_system_name
    )

    scan_result = DeviceOperationsProvider().virus_scan_device(
        configuration.mountpoint_path
    )
    SystemOperationsProvider().unmount_device(logger, mounted_device_partition)
    DeviceOperationsProvider().handle_kernel_driver(device_handle, False)

    return scan_result
