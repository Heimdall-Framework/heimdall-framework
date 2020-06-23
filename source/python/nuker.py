import subprocess

class Nuker():
    def __init__(self, partition):
        self.__nukable_partition = partition

    def nuke(self):
        nuking_command = 'dd if=/dev/zero of={} bs=8192'.format(self.__nukable_partition)
        
        process = subprocess.Popen(
            nuking_command.split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )

        result, error = process.communicate()

        if error != None:
            return False
        return True