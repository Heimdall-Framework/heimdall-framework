import tkinter as tk
import math
from pymsgbox import alert
from usb_detector import USBHotplugDetector

FONT_LARGE = ('Verdona', 16)
FONT_SMALL = ('Verdona', 12)


class HeimdallApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, 'Heimdall')

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, ConfigPage):
            frame = F(container, self)
            
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')
        
        self.show_frame(StartPage)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        usb_detector = USBHotplugDetector() 

        # navigation menu:
        evaluator_page_btn = tk.Button(
            self,
            text='Evaluator',
            command = None
        )
        evaluator_page_btn.grid(column=0, row=0)

        config_page_btn = tk.Button(
            self,
            text='Configs',
            command = lambda:controller.show_frame(ConfigPage)
        )
        config_page_btn.grid(column=1, row=0)
        
        # page content:
        label = tk.Label(
            self, 
            text='Heimdall - Main', 
            font=FONT_LARGE
            )
        label.grid(column=2, row=1)

        start_evaluator_btn = tk.Button(
            self,
            text='Start Evaluator',
            command = usb_detector.start
            )
        start_evaluator_btn.grid(column=2, row=2)
        
        stop_evaluator_btn = tk.Button(
            self,
            text='Stop Evaluator', 
            command = usb_detector.stop
            )
        stop_evaluator_btn.grid(column=2, row=3)

        log_label = tk.Label(
            self, 
            text='Logs:', 
            font=FONT_SMALL
            )
        log_label.grid(column=0, row=4)

        log_textbox = tk.Text(
            self,
            height=40,
            width= 100
        )
        log_textbox.grid(column=0, row=5)

class ConfigPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

       # navigation menu:
        evaluator_page_btn = tk.Button(
            self,
            text='Evaluator',
            command = lambda: controller.show_frame(StartPage)
        )
        evaluator_page_btn.grid(column=0, row=0)

        config_page_btn = tk.Button(
            self,
            text='Configs',
            command = None
        )
        config_page_btn.grid(column=1, row=0)
        
        # page content:
        label = tk.Label(
            self,
            text='Heimdall - Config', 
            font=FONT_LARGE
            )
        label.grid(column=2, row=1)

def show_msg_box(box_title, box_content, buttons = 'Okay'):
    alert(box_content, box_title, buttons)