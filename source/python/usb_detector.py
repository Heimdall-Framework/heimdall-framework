import usb1 as usb
from logger import log
from evaluator import Evaluator
from queue import Queue
import gui_elements
from device_operations_provider import DeviceOperationsProvider

SERVICE_PORTS = [0,2]
TEST_PORTS = [1,3]

class USBHotplugDetector():
    def __init__(self):
        self.__cached_device = None

    def start(self):
        self.__is_started = True
        self.__begin_detecting()

    def stop(self):
        self.__is_started = False
        print('stoped')

    def __begin_detecting(self):
        log(">>> Hotplug detector was started.")
        with usb.USBContext() as context:
            while self.__is_started:
                # finds a new device that can be tested
                device = DeviceOperationsProvider().find_new_device(
                    TEST_PORTS,
                    context
                )

                # checks if the found device has already been tested
                if self.__cached_device == device or device is None:
                    continue

                # creates USBDeviceHandle object for given VID and PID
                handle = context.openByVendorIDAndProductID(
                    device.getVendorID(),
                    device.getProductID(),
                    skip_on_error=True
                )

                # checks if the device is still present ot if the user is allowed to access it
                if handle is None:
                    log(">>> Device not present, or user is not allowed to use the device.")
                else:
                    # detaches device's kernel driver
                    DeviceOperationsProvider().handle_kernel_driver(handle, False)

                    # creates Evaluator object with given USBDeviceHandlem, USBDevice and device's USBContext
                    evaluator = Evaluator(
                        handle,
                        device.getPortNumber(),
                        context
                        )

                    if not evaluator.test_device():
                        log(">>>! DEVICE IS NOT SAFE !<<<")
                        gui_elements.show_msg_box('Dangerous device detected','Tested device is not safe for use.')

                        handle.close()
                        evaluator = None

                        self.__cached_device = device
                    else:
                        log(">>> Device is SAFE for use")
                        handle.close()
                        evaluator = None

                        self.__cached_device = device
            print(">>> Hotplug detector was terminated.")