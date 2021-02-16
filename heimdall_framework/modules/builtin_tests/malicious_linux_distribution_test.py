import os
from heimdall_framework.modules.device_operations_provider import DeviceOperationsProvider
from heimdall_framework.modules.system_operations_provider import SystemOperationsProvider
from heimdall_framework.modules.file_operations_provider import FileOperationsProvider


def run(logger, configuration, device, device_handle):
    DeviceOperationsProvider().handle_kernel_driver(device_handle, True)

    device_system_name = DeviceOperationsProvider().get_device_udev_property(
        device, device_handle,  "DEVNAME"
    )
    _, mounted_device_partition = SystemOperationsProvider().mount_device(
        configuration, logger, device_system_name
    )

    indicator_file_path = FileOperationsProvider().find_file(
        configuration, configuration.mounting_point, "tails.cfg"
    )

    if indicator_file_path is None:
        logger.log(
            "> Indicator file does not exist in the filesystem. Test is being flaged as successful."
        )
        SystemOperationsProvider().unmount_device(logger, mounted_device_partition)

        return True
    else:
        logger.log("> Test not implemented. Skipping.")

        return True
