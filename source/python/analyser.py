def is_being_plugged(device):
    if device.action == "add":
        return True
    else:
        return False