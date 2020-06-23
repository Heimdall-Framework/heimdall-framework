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
from logger import Logger

class SystemOperationsProvider():
    def __init__(self):
        self.device_mountpoint = os.environ['DEVS_MOUNTPOINT']

    # mounts the device on predetermined point with noexec and rw permission parameters
    def mount_device(self, device_system_name, current_part=0):
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

    def unmount_device(self, mounted_device_partition,):
        mounting_command = 'umount {}'.format(mounted_device_partition)
        process = subprocess.Popen(
            mounting_command.split(), 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT
            )

        output, error = process.communicate()
        
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
    
    # returns the checksum of a file for a given file path
    def get_file_checksum(self, file_path):
        command = 'sha256sum {}'.format(file_path)

        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, error = process.communicate()
        
        if error != None:
            Logger().log(error)
            return None
        return output

    # checks if Tails iso checksum is blackslisted as dangerous
    def offline_verify_checksum(self, checksum):
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