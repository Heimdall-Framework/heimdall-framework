import os 
import filecmp
import subprocess
from subprocess import check_output
from logger import Logger

initrd_list = ['initrd', 'initrd.img', 'initrd.gz']

class FileOperationsProvider():
    
    # compares two files
    def compare_files(self, firstFilePath, secondFilePath):
        return filecmp.cmp(firstFilePath, secondFilePath)

    # finds the initial ramdisk file on a liveboot
    def find_initrd(self, directory):
        for root, dirs, files in os.walk(directory):
            for f in files:
                if f in initrd_list:
                    return '{0}/{1}'.format(root, f)

    def create_img_file(self):
        creation_command = 'mkisofs -o /tmp/temp_image.img /home/ivan/mount_point'
        process = subprocess.Popen(creation_command.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        
        output, error = process.communicate()
        if error != None:
            Logger().log(error)
            return False
        
        return True
