import os 
from datetime import datetime

DUMP_FILES_DIRECTORY_PATH = os.environ['DUMPS_DIRECTORY_PATH']

def log(string, silent=False):
    current_datetime = datetime.now()
    
    if not os.path.exists(DUMP_FILES_DIRECTORY_PATH):
        os.mkdir(DUMP_FILES_DIRECTORY_PATH)
    
    logfile_name = '%s/LOG_%s_%s_%s'%(DUMP_FILES_DIRECTORY_PATH, current_datetime.year, current_datetime.month, current_datetime.day)
    
    file = open(logfile_name + '.log' , 'a+') 

    file.write('[' + str(current_datetime.timestamp()) + ']' + string  + '\r\n')
    
    # doesn't print the log if the silent flag is set to True
    if not silent:
        print(string)

    file.close()