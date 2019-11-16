import os 
import filecmp

initrd_list = ['initrd', 'initrd.img', 'initrd.gz']

class FileOperationsProvider:
    def compare_files(self, firstFilePath, secondFilePath):
        return filecmp.cmp(firstFilePath, secondFilePath)

    def find_initrd(self, directory):
        for root, dirs, files in os.walk(directory):
            for f in files:
                if f in initrd_list:
                    return '{0}/{1}'.format(root, f)
