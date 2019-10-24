import os 
from datetime import datetime

DUMP_FILES_DIRECTORY_PATH = '/heimdall_dumps'

def log(string):
    current_datetime = datetime.now()
    
    if not os.path.exists(DUMP_FILES_DIRECTORY_PATH):
        os.mkdir(DUMP_FILES_DIRECTORY_PATH)
    
    dumpfile_name = '%s/LOG_%s_%s_%s'%(DUMP_FILES_DIRECTORY_PATH, current_datetime.year, current_datetime.month, current_datetime.day)
    
    file = open(dumpfile_name + '.log' , 'a+') 

    file.write('[' + str(current_datetime.timestamp()) + ']' + string  + '\r\n')
        
    print(string)

    file.close()