from pymsgbox import alert, confirm

class GuiProvider():
    def __init__(self):
        pass

    def show_msg_box(self, box_title, box_content, buttons = 'Okay'):
        alert(box_content, box_title, buttons)

    def show_confirm_box(self, box_title, box_content, displayed_buttons = ['Yes', 'No']):
        result = confirm(text=box_content, title=box_title, buttons=displayed_buttons)

        if result == displayed_buttons[0]:
            return True
        else:
            return False
            