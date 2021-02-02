import os
import sys
from datetime import datetime


class Logger():
    def __init__(self, logs_directory_path: str):
        self.__logs_directory_path = logs_directory_path

    def log(self, string, silent=False):
        current_datetime = datetime.now()

        if not os.path.exists(self.__logs_directory_path):
            os.mkdir(self.__logs_directory_path)

        logfile_name = '%s/LOG_%s_%s_%s' % (self.__logs_directory_path,
                                            current_datetime.year, current_datetime.month, current_datetime.day)

        file = open(logfile_name + '.log', 'a+')

        file.write(
            '[' + str(current_datetime.timestamp()) + ']' + string + '\r\n')

        # Does not print the log if the silent flag is raised
        if not silent:
            print(string)

        file.close()

    def log_error(self, *args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)
