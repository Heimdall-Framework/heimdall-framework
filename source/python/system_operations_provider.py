import os
import time
import datetime
import ctypes
import ctypes.util

class SystemOperationsProvider():
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

class timespec_struct(ctypes.Structure):
    _fields_ = [
        ('tv_sec', ctypes.c_long),
        ('tv_nsec', ctypes.c_long)
    ]