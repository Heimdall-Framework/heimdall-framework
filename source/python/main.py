import usb1 as usb
import tkinter as tk
from logger import log
from evaluator import Evaluator
from gui_elements import show_msg_box
from device_operations_provider import DeviceOperationsProvider

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
        
        label = tk.Label(
            self, 
            text='Heimdall - Main', 
            font=FONT_LARGE
            )
        label.pack(pady=5, padx=5)
        
        evaluator = Starter() 

        startEvaluator = tk.Button(
            self,
            text='Start Evaluator',
            command=evaluator.start
            )
        startEvaluator.pack(pady=5, padx=5)

        stopEvaluator = tk.Button(
            self, 
            text='Stop Evaluator', 
            command = evaluator.stop
            )
        stopEvaluator.pack(pady=5, padx=5)

class ConfigPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(
            self, 
            text='Heimdall - Config', 
            font=FONT_LARGE
            )
        label.pack(pady=5, padx=5)

class Starter():
    def __init__(self):
        self.__is_initiating = True
        self.__cached_devices = []
        
    def start(self):
        self.__is_started = True
        self.__start_evaluator()
    def stop(self):
        self.__is_started = False

    def __start_evaluator(self):
        while self.__is_started:
            with usb.USBContext() as context:
                device_list = context.getDeviceList()
                
                if not self.__is_initiating:
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

                                    tester = Evaluator(
                                        handle, 
                                        device.getPortNumber(), 
                                        context
                                        )
                                    
                                    if not tester.test_device():
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
                    self.__is_initiating = False

app = HeimdallApp()
app.attributes('-fullscreen', True)
app.mainloop()