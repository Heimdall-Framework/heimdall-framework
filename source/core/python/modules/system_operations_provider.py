import os
import pwd
import time
import ctypes
import getpass
import datetime
import subprocess
import ctypes.util
from subprocess import check_output
from collections import namedtuple
from .logger import Logger

class SystemOperationsProvider():
    def __init__(self):
        self.device_mountpoint = os.environ['DEVS_MOUNTPOINT']
    
    def rebuild_package(self, setup_file_location: str) -> bool:
        """
        Reinstalls the framework after update.
        
        :param setup_file_location: the location of the setup.py file
        """
        rebuild_command = "pip3 install -e ."
        command_execution_proccess = subprocess.Popen(rebuild_command.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        output, error = command_execution_proccess.communicate()

        if error != None:
            return False
        return True

    def mount_device(self, device_system_name: str, current_part=0):
        """
        Mount the device on a predetermined mountpoint with noexec and rw permission parameters
        
        :param device_system_name: The system name of the device
        :param current_partition: The device partition that is being currently mounted
        """

        mounting_command = 'mount {}{} {} -o noexec'.format(device_system_name, current_part, self.device_mountpoint)
        process = subprocess.Popen(mounting_command.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, error = process.communicate()

        if 'bad' in str(output) or 'not exist' in str(output) and current_part == 0:
            for i in range(1, 10):
                if self.mount_device(device_system_name, current_part=i):
                    return True, device_system_name+str(i)
            return False, None
    
        if error != None:
            Logger().log(error)
            return False, None
    
        return True, device_system_name+str(current_part)

    def unmount_device(self, mounted_device_partition: str) -> bool:
        """
        Unmounts a device's partition

        :param mounted_device_partition: The system name of the partition 
        """

        mounting_command = 'umount {}'.format(mounted_device_partition)
        process = subprocess.Popen(
            mounting_command.split(), 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT
            )

        _, error = process.communicate()
        
        Logger().log('Device was unmounted.',silent=True)

        if error != None:
            Logger().log(error)
            return False
        
        return True

    # changes system clock time to a given one
    def change_system_time(self, required_time):
        OS_CLOCK_REALTIME_ID = 0

        librt = ctypes.CDLL(ctypes.util.find_library('rt'))
        
        timespec = timespec_struct()
        timespec.tv_sec = int(time.mktime(datetime.datetime(*required_time[:6].timetuple())))
        timespec.tv_nsec = required_time[6] * 1000000

        librt.clock_settime(
            OS_CLOCK_REALTIME_ID, 
            ctypes.byref(timespec)
            )
    
    def get_file_checksum(self, file_path):
        """
        Retrives a file's checksum

        :param file_path: The path to the file
        """

        command = 'sha256sum {}'.format(file_path)

        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, error = process.communicate()
        
        if error != None:
            Logger().log(error)
            return None
        return output

    def offline_verify_checksum(self, checksum):
        """
        Verifies if a Tails image checksum is blacklisted as dangerous

        :param checksum: The checksum of the image
        """

        with open(os.path.dirname(os.path.realpath(__file__))+ '/blacklisted.blck') as blacklisted:
            if not checksum in blacklisted:
                return True
            else:
                return False

# timespec structure
class timespec_struct(ctypes.Structure):
    _fields_ = [
        ('tv_sec', ctypes.c_long),
        ('tv_nsec', ctypes.c_long)
    ]