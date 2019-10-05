import os 
import filecmp

def is_being_plugged(device):
    if device.action == "add":
        return True
    else:
        return False

def compare_files(firstFile, secondFile):
    return filecmp.cmp(firstFile, secondFile)

def find_initrd(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == 'initrd':
                return '{0}/{1}'.format(root, file)