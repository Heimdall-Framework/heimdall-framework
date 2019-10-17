import tkinter as tk
import usb1 as usb
import device_operations as dops
import analyser
from device_operations import DeviceOperationsProvider
from tester import Tester
from gui_elements import show_msg_box
from logger import log

SERVICE_PORTS = [0,2]
UNPLUGGING_TESTS_COUNT = 4

FONT_LARGE = ('Verdona', 14)

class HeimdallApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.frames = {}
        frame = StartPage(container, self)
        
        self.frames[StartPage] = frame
        frame.grid(row=0, column=0, sticky='nsew')
        
        self.show_frame(StartPage)

    def show_frame(self, controller):
        frame = self.frames[controller]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Heimdall', font=FONT_LARGE)
        label.pack(pady=5, padx=5)

        button = tk.Button(self, cnf="Start Threat Evaluator")
        button.pack(pady=5, padx=5)


is_initiating = True
cached_devices = []

while True:
    with usb.USBContext() as context:
        device_list = context.getDeviceList()
        
        if not is_initiating:
            #if cached devices count is less than the real count of conencted devices
            if cached_devices is None or len(device_list) < len(cached_devices):
                #caches the currently currently connected devices in a collection
                cached_devices = device_list

            #if real count of connected devices is more tha the count of the cached ones
            elif len(device_list) > len(cached_devices):
                #creates a list that contains only the newly connected devices
                new_devices = DeviceOperationsProvider().find_new_device(
                    cached_devices,
                    device_list
                    )
                
                #caches the new devices
                cached_devices = device_list
                
                #lists the newly connected devices
                for device in new_devices:                                             
                    #creates a handler for a given USB context
                    handle = context.openByVendorIDAndProductID(
                        device.getVendorID(), 
                        device.getProductID(), 
                        skip_on_error=True
                        )

                    if handle is None:
                        log(">>> Device not present, or user is not allowed to use the device.")
                    else:
                        DeviceOperationsProvider().handle_kernel_driver(handle, False)
                        
                        if device.getPortNumber() not in SERVICE_PORTS:
                            log(">>> Test device was connected. Initiating testing procedure...")

                            tester = Tester(
                                handle, 
                                device.getPortNumber(), 
                                context
                                )
                            
                            if tester.test_device() != True:
                                log(">>>!!! DEVICE IS NOT SAFE !!!<<<")
                                
                                handle.close()
                                tester = None
                            else:
                                log(">>> Device is SAFE for use")
                                
                                handle.close()
                                tester = None
                        else:
                            DeviceOperationsProvider().handle_kernel_driver(handle, True)
                            log(">>> Service device was connected.")
                                     
        else:
            cached_devices = device_list
            is_initiating = False