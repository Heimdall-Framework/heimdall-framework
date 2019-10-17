from pymsgbox import alert
import tkinter

def show_msg_box(box_title, box_content, buttons = 'Okay'):
    alert(box_content, box_title, buttons)
