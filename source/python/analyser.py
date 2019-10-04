import filecmp
def is_being_plugged(device):
    if device.action == "add":
        return True
    else:
        return False

def compare_files(firstFile, secondFile):
    return filecmp.cmp(firstFile, secondFile)