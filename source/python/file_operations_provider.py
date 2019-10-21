import os 
import filecmp

class FileOperationsProvider:
    def compare_files(self, firstFilePath, secondFilePath):
        return filecmp.cmp(firstFilePath, secondFilePath)

    def find_initrd(self, directory):
        for root, dirs, files in os.walk(directory):
            for f in files:
                if f == 'initrd':
                    return '{0}/{1}'.format(root, f)
