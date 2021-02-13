import os
import shutil
from heimdall_framework.modules.data_provider import DataProvider
from heimdall_framework.modules.device_operations_provider import (
    DeviceOperationsProvider,
)
from heimdall_framework.modules.system_operations_provider import (
    SystemOperationsProvider,
)
from heimdall_framework.modules.file_operations_provider import FileOperationsProvider


def run(logger, configuration, device, device_handle):
    """
    Scan tested device for viruses.
    """

    logger.log('> Retrieving device system name.')
    device_system_name = DeviceOperationsProvider().get_device_udev_property(
        device, device_handle, "DEVNAME"
    )

    logger.log('> Mounting main device partition.')
    _, mounted_device_partition = SystemOperationsProvider().mount_device(
        configuration, logger, device_system_name
    )

    logger.log('> Launching ClamAV scan.')
    scan_result = DeviceOperationsProvider().virus_scan_device(
        configuration.mounting_point,
        logger
    )

    logger.log('> Unmounting main device partition.')
    SystemOperationsProvider().unmount_device(logger, mounted_device_partition)

    logger.log('> Detaching device driver.')
    DeviceOperationsProvider().handle_kernel_driver(device_handle, False)

    return scan_result
