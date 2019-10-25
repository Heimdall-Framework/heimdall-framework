import os 
from datetime import datetime

dump_files_directory_path = '/heimdall_dumps'

def log(string):
    current_datetime = datetime.now()
    
    if not os.path.exists(dump_files_directory_path):
        os.mkdir(dump_files_directory_path)
    
    dumpfile_name = '%s/LOG_%s_%s_%s'%(dump_files_directory_path, current_datetime.year, current_datetime.month, current_datetime.day)
    
    file = open(dumpfile_name + '.log' , 'a+') 

    file.write('[' + str(current_datetime.timestamp()) + ']' + string  + '\r\n')
        
    print(string)

    file.close()