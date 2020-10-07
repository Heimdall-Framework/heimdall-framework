import subprocess

class Nuker():
    def __init__(self, partition: str):
        self.__nukable_partition = partition

    def nuke(self) -> None:
        """
        Rewrites a disk or a partition with a random set of bytes.
        """

        nuking_command = 'dd if=/dev/random of={} bs=8192'.format(self.__nukable_partition)
        
        process = subprocess.Popen(
            nuking_command.split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
 
        _, error = process.communicate()

        if error != None:
            return False
        return True