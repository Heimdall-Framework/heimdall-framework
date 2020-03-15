import os 
from datetime import datetime

class Logger():
    def __init__(self):
        self.logs_directory_path= os.environ['LOGS_DIRECTORY_PATH']

    def log(self, string, silent=False):
        current_datetime = datetime.now()
        
        if not os.path.exists(self.logs_directory_path):
            os.mkdir(self.logs_directory_path)
        
        logfile_name = '%s/LOG_%s_%s_%s'%(self.logs_directory_path, current_datetime.year, current_datetime.month, current_datetime.day)
        
        file = open(logfile_name + '.log' , 'a+') 

        file.write('[' + str(current_datetime.timestamp()) + ']' + string  + '\r\n')
        
        # doesn't print the log if the silent flag is set to True
        if not silent:
            print(string)

        file.close()