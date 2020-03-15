import os
import time
import datetime
import ctypes
import ctypes.util
import subprocess
from subprocess import check_output
from collections import namedtuple
from logger import Logger


DEVICE_MOUNTPOINT = '/home/ivan/mount_point'

class SystemOperationsProvider():
    
    # mounts the device on predetermined point with noexec and rw permission parameters
    def mount_device(self, device_system_name, current_part=0):
        mounting_command = 'sudo mount {}{} {} -o noexec'.format(device_system_name, current_part, DEVICE_MOUNTPOINT)

        process = subprocess.Popen(mounting_command.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, error = process.communicate()
        
        if 'bad' in str(output) or 'not exist' in str(output) and current_part == 0:
            for i in range(1, 10):
                if self.mount_device(device_system_name, current_part=i):
                    return True
                return False

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
        command = 'sha256sum {}'.format(file_path)

        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, error = process.communicate()
        if error != None:
            Logger().log(error)
            return None
        return output

    def offline_verify_checksum(self, checksum):
        with open('/home/ivan/Documents/Projects/cybersecurity/heimdall/source/python/blacklisted.blck') as blacklisted:
            if not checksum in blacklisted:
                return True
            else:
                return False

class timespec_struct(ctypes.Structure):
    _fields_ = [
        ('tv_sec', ctypes.c_long),
        ('tv_nsec', ctypes.c_long)
    ]