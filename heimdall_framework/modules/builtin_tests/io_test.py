import os
import shutil
from heimdall_framework.modules.data_provider import DataProvider
from heimdall_framework.modules.device_operations_provider import DeviceOperationsProvider
from heimdall_framework.modules.system_operations_provider import SystemOperationsProvider
from heimdall_framework.modules.file_operations_provider import FileOperationsProvider


def run(logger, configuration, device, device_handle):
    DeviceOperationsProvider().handle_kernel_driver(device_handle, True)

    device_system_name = DeviceOperationsProvider().get_device_udev_property(device,
                                                                             device_handle, 'DEVNAME')

    _, mounted_device_partition = SystemOperationsProvider(
    ).mount_device(configuration, logger, device_system_name)

    process_files(logger, configuration, ['pdf', 'exe', 'bin', 'doc', 'xlm'])

    SystemOperationsProvider().unmount_device(logger, mounted_device_partition)
    DeviceOperationsProvider().handle_kernel_driver(device_handle, False)

    return False


def process_files(logger, configuration, file_types):
    for file_type in file_types:
        dump_file_name = 'dump.{}'.format(file_type)
        dump_file_location = os.path.join(
            os.path.dirname(__file__), dump_file_name)

        DataProvider().generate_random_data_file(logger, dump_file_location)

        shutil.copyfile(
            dump_file_location,
            os.path.join(configuration.mounting_point, dump_file_name)
        )
        shutil.move(
            os.path.join(configuration.mounting_point, dump_file_name),
            'received_dump.{}'.format(file_type)
        )

        if not FileOperationsProvider().compare_files('dump.me', 'received_dump.{}'.format(file_type)):
            os.remove(dump_file_name)
            os.remove('received_dump.{}'.format(file_type))

            return False

        os.remove(dump_file_name)
        os.remove('received_dump.{}'.format(file_type))

    return True
