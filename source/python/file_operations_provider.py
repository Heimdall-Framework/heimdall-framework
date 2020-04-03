import os 
import filecmp
import subprocess
from subprocess import check_output
from logger import Logger


class FileOperationsProvider():
    def __init__(self):
        self.device_mountpoint = os.environ['DEVS_MOUNTPOINT']
    # compares two files
    def compare_files(self, firstFilePath, secondFilePath):
        return filecmp.cmp(firstFilePath, secondFilePath)

    # recursively searches for a specific file that identifies the partition as a liveboot distribution of Tails
    def find_file(self, directory, file):
        for dir_path, directories, files in os.walk(directory, followlinks=True):
            for sub_dir in directories:
                self.find_file(self.device_mountpoint + sub_dir, file)

            for file_name in files:
                if file_name.lower == str(file).lower:
                    return dir_path + file_name
        return None

    # packs the contents of the mount directory into a disk image file
    def create_img_file(self, extension):
        creation_command = 'mkisofs -o /tmp/temp_image.{} {}'.format(extension, os.environ['DEVS_MOUNTPOINT'])
        process = subprocess.Popen(creation_command.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        
        output, error = process.communicate()
        if error != None:
            Logger().log(error)
            return False
        
        return True
