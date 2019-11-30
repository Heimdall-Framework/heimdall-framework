import os 
from datetime import datetime

dump_files_directory_path = '/heimdall_dumps'

def log(string):
    current_datetime = datetime.now()
    
    if not os.path.exists(dump_files_directory_path):
        os.mkdir(dump_files_directory_path)
    
    logfile_name = '%s/LOG_%s_%s_%s'%(dump_files_directory_path, current_datetime.year, current_datetime.month, current_datetime.day)
    
    file = open(logfile_name + '.log' , 'a+') 

    file.write('[' + str(current_datetime.timestamp()) + ']' + string  + '\r\n')
        
    print(string)

    file.close()

def read_log():
    current_datetime = datetime.now()

    logfile_name = '%s/LOG_%s_%s_%s'%(dump_files_directory_path, current_datetime.year, current_datetime.month, current_datetime.day)

    file = open(logfile_name + '.log' , 'r') 

    return file.read()

    