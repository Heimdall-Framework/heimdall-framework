import tkinter as tk
import math
from pymsgbox import alert

def show_msg_box(box_title, box_content, buttons = 'Okay'):
    alert(box_content, box_title, buttons)