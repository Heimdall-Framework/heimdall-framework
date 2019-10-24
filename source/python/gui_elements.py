import tkinter as tk
from pymsgbox import alert
from usb_detector import USBHotplugDetector

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
        
        usb_detector = USBHotplugDetector() 

        startEvaluator = tk.Button(
            self,
            text='Start Evaluator',
            command = usb_detector.start
            )
        startEvaluator.pack(pady=5, padx=5)

        stopEvaluator = tk.Button(
            self,
            text='Stop Evaluator', 
            command = usb_detector.stop
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


def show_msg_box(box_title, box_content, buttons = 'Okay'):
    alert(box_content, box_title, buttons)