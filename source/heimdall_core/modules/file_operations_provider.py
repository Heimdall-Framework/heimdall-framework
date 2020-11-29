import os 
import mmap
import filecmp
import subprocess
from subprocess import check_output
from .logger import Logger


class FileOperationsProvider():
    def __init__(self):
        self.device_mountpoint = os.environ['DEVS_MOUNTPOINT']

    def compare_files(self, first_file_path, second_file_path):
        """
        Compare two files

        :param first_file_path: The path to first file that will be compared
        :param second_file_path: The path to first file that will be compared
        """
        
        return filecmp.cmp(first_file_path, second_file_path)

    def find_file(self, directory, file):
        """
        Recursively search for a specific file.

        :param directory: The directory that will be searched
        :param file: The file that it is being looked for
        """

        for dir_path, directories, files in os.walk(directory, followlinks=True):
            for sub_dir in directories:
                self.find_file(self.device_mountpoint + sub_dir, file)

            for file_name in files:
                if file_name.lower == str(file).lower:
                    return dir_path + file_name
        return None

    def file_contains_string(self, string, file_path):
        """
        Checks if a file contains a string.
        Returns True if yes and False if no.

        :param string: The string that will be searched for 
        :param file_path: The path to the file that will be searched
        """

        with open(file_path) as file:
            file_string_object = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
            return file_string_object.find(string) != -1

    def create_img_file(self, logger, extension):
        """
        Packs the contents of the mount directory into a disk image file

        :param extension: The file extension that will be used (iso or img) 
        """

        creation_command = 'mkisofs -o /tmp/temp_image.{} {}'.format(extension, os.environ['DEVS_MOUNTPOINT'])
        process = subprocess.Popen(creation_command.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        
        output, error = process.communicate()
        if error != None:
            logger.log(error)
            return False
        
        return True
