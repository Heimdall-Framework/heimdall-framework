import os
from heimdall_framework.modules.device_operations_provider import DeviceOperationsProvider 
from heimdall_framework.modules.system_operations_provider import SystemOperationsProvider
from heimdall_framework.modules.file_operations_provider import FileOperationsProvider

def run(logger, configuration, device, device_handle):
    DeviceOperationsProvider().handle_kernel_driver(device_handle, True)

    device_system_name = DeviceOperationsProvider().get_device_udev_property(device, 'DEVNAME')
    _, mounted_device_partition = SystemOperationsProvider().mount_device(configuration, logger, device_system_name)
    
    indicator_file_path = FileOperationsProvider().find_file(configuration, configuration.mounting_point, 'tails.cfg')

    if indicator_file_path is None:
        logger.log('> Indicator file does not exist in the filesystem. Test is being flaged as successful.')
        SystemOperationsProvider().unmount_device(logger, mounted_device_partition)        

        return True
    else:
        logger.log('> Packing live boot files into image file.')
        FileOperationsProvider().create_img_file(logger, 'img')
        FileOperationsProvider().create_img_file(logger, 'iso')

        logger.log('> Generating image file checksum.')

        local_image_checksum = str(SystemOperationsProvider().get_file_checksum(logger, '/tmp/temp_image.img'))

        # compares the checksums from the Tails website to the local one
        if SystemOperationsProvider().offline_verify_checksum(local_image_checksum):
            os.remove('/tmp/temp_image.img')
            os.remove('/tmp/temp_image.iso')

            SystemOperationsProvider().unmount_device(logger, mounted_device_partition)        
            return True
        else:
            os.remove('/tmp/temp_image.img')
            os.remove('/tmp/temp_image.iso')
            logger.log('> The Tails image is outdated or has been altered. Please update your Tails liveboot to the newest version and test again.')
            
            SystemOperationsProvider().unmount_device(logger, mounted_device_partition)                        
            return False