import usb1 as usb
from .logger import Logger
from .nuker import Nuker
from .logger import Logger
from .evaluator import Evaluator
from .gui_provider import GuiProvider
from .device_operations_provider import DeviceOperationsProvider

class USBHotplugDetector:
    def __init__(self, configuration, logger):
        self._configuration = configuration
        self._logger = logger
        self._testing_ports = configuration.testing_ports
        self._nuking_ports = configuration.nuking_ports
        self._cached_device = None
        self._nuked_device = None
        self._tested_device = None

    def start(self):
        self._is_started = True
        self._begin_detecting()

    def stop(self):
        self._is_started = False
        print(">>> Hotplug detector was stopped.")

    def _begin_detecting(self):
        self._logger.log(">>> Hotplug detector was started.")

        try:
            with usb.USBContext() as context:
                while self._is_started:
                    # finds a new device that can be tested
                    device = DeviceOperationsProvider().find_new_device(
                        self._testing_ports, self._nuking_ports, context
                    )

                    # checks if the found device has already been tested
                    if (
                        device is None
                        or device == self._tested_device
                        or device == self._nuked_device
                    ):
                        continue

                    # creates USBDeviceHandle object for given VID and PID
                    handle = context.openByVendorIDAndProductID(
                        device.getVendorID(), device.getProductID(), skip_on_error=True
                    )

                    DeviceOperationsProvider().handle_kernel_driver(handle, False)

                    # checks if the device is still present ot if the user is allowed to access it
                    if handle is None:
                        self._logger.log(
                            ">>> Device not present or user is not allowed to use the device."
                        )
                    else:
                        if device.getPortNumber() in self._nuking_ports:
                            if GuiProvider().show_confirm_box(
                                "Nuking Alert",
                                "You will not be able to recover the data from the nuked device. \nDo you want to proceed?",
                            ):
                                self._nuke_device(device)
                        elif device.getPortNumber() in self._testing_ports:
                            (
                                evaluation_result,
                                evaluated_device,
                            ) = self._evaluate_device(device, handle, context)

                            # indicates that the tested device is NOT safe for use
                            if not evaluation_result:
                                self._logger.log(">>>! DEVICE IS NOT SAFE !<<<")
                                GuiProvider().show_msg_box(
                                    "Dangerous device detected",
                                    "The tested device is NOT safe for use.",
                                )

                            # indicates that the tested device is safe for use
                            else:
                                self._logger.log(">>> Device is SAFE for use")
                                GuiProvider().show_msg_box(
                                    "Passed",
                                    "All tests were passed. The tested device is safe for use.",
                                )

                            self._cache_tested_device(evaluated_device)
                        handle.close()

                self._logger.log(">>> Hotplug detector was terminated.")

        except usb.USBError as err:
            self._logger.log(">>> An exception has occurred")
            self._logger.log(">>> More information: " + str(err))

    def _evaluate_device(self, device, handle, context):
        # creates Evaluator object with given USBDeviceHandlem, USBDevice and device's USBContext
        evaluator = Evaluator(
            self._configuration, self._logger, handle, device.getPortNumber(), context
        )

        result, returned_device = evaluator.evaluate_device()

        evaluator = None
        return result, returned_device

    def _nuke_device(self, device):
        device_partition = DeviceOperationsProvider().get_device_udev_property(
            device, "DEVNAME"
        )
        nuker = Nuker(device_partition)

        self._logger.log(">> Nuking device on port: {}".format(device.getPortNumber()))

        self._logger.log(">> Hang tight, it will take some time.")
        nuker.nuke()

        self._logger.log(">>> Nuking finished.")

        # cacheing fake device in order to allow testing for the same device immediately after nuking
        self._cache_nuked_device(device)
        self._cache_tested_device(None)

    # caches the device that was just tested
    def _cache_tested_device(self, device):
        self._tested_device = device

    # caches the device that was just nuked
    def _cache_nuked_device(self, device):
        self._nuked_device = device
