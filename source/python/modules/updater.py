import os
import sys
import json
import shutil
import tarfile
import urllib
import requests
from .logger import Logger

TEMP_DIR_NAME = '/tmp/temp_update_data/'

class Updater():
    def __init__(self, framework_location, update_url):
        self.framework_location = framework_location
        self.version_logs_location = framework_location + '/update_logs/versions.json'
        self.plugins_directory_location = framework_location + '/plugins/'
        self.update_url = update_url
        self.updated_files_counter = 0

    def update(self):
        '''
        Update the running version of the framework or it's plugins if newer ones exist.
        Return True or False, depending on the outcome of the operation.
        '''
        
        try:
            is_new = True
            self.device_serial_number = self.__get_device_serial_number()

            if self.device_serial_number == 'FAIL':
                return False
            
            self.__load_update_logs()
            self.__load_plugins_config()

            available_updates = self.__get_available_updates()
            
            for update in available_updates:
                for local_update_log in self.update_logs:
                    if update['name'] == local_update_log['name']:
                        is_new = False

                        if update['version'] != local_update_log['version']:
                            download_link = self.__get_download_link(
                                update['name'],
                                update['version'],
                                update['type']
                            )

                        if update['type'] == 'plugin':
                            self.__process_update(download_link, True)
                        else:
                            self.__process_update(download_link, False)

                        local_update_log['version'] = update['version']
                        break
                
                if is_new:
                    download_link = self.__get_download_link(
                        update['name'],
                        update['version'],
                        update['type']
                    )

                    if update['type'] == 'plugin':
                        self.__process_update(download_link, True)
                    else:
                        self.__process_update(download_link, False)


                    self.update_logs.append({
                        'name' : update['name'],
                        'version' : update['version'],
                        'type' : update['type']
                    })

                    self.__update_plugins_config(update['name'])
                    
                    break

                is_new = True

            with open(self.version_logs_location, 'w') as update_logs_file:
                update_logs_file.write(json.dumps(self.update_logs))     
            return True
        except:
            raise
            return False

    def __load_update_logs(self):
        with open(self.version_logs_location, 'r') as update_logs_file:
            self.update_logs = json.loads(update_logs_file.read() or '[]')

    def __load_plugins_config(self):
        with open(self.plugins_directory_location + '/config.json') as plugins_config:
            self.plugins_config = json.loads(plugins_config.read() or '[]')

    def __get_available_updates(self):
        parameters = {
            'action' : 'info',
            'device_serial_number' : self.device_serial_number
        }

        response = requests.get(self.update_url, params=urllib.parse.urlencode(parameters))

        if response.status_code == 422:
            Logger().log('>>> Wrong parameters. Aborting update!')

        return response.json()

    def __process_update(self, download_url, is_plugin):
        try:
            self.updated_files_counter += 1

            if not os.path.isdir(TEMP_DIR_NAME):
                os.mkdir(TEMP_DIR_NAME)

            urllib.request.urlretrieve(download_url, TEMP_DIR_NAME + '/update.tar.gz')

            archive = tarfile.open(TEMP_DIR_NAME + '/update.tar.gz', "r:gz")
            archive.extractall()
            archive.close()

            for dir_path, dir_name, file_names in os.walk(TEMP_DIR_NAME):
                for file_name in file_names:
                    if is_plugin and file_name.endswith('.py') or file_name.endswith('.pyc'):
                        shutil.move(
                            TEMP_DIR_NAME + file_name, 
                            self.plugins_directory_location
                            )
                    else:
                        shutil.move(
                            TEMP_DIR_NAME + file_name, 
                            self.framework_location
                            )
                        
            
            shutil.rmtree(TEMP_DIR_NAME)
            return True
        except:
            shutil.rmtree(TEMP_DIR_NAME)
            Logger().log('>>> Processing update failed.')

            return False
            

    def __update_plugins_config(self, plugin_name):
        self.plugins_config.append({
            'name' : plugin_name,
            'main_function' : 'main',
            'enabled' : True
        })

    def __get_download_link(self, update_name, update_version, update_type):
        '''
        Get the download link for update.

        :param update_name: the name of the update
        :param update_version: the version of the update
        :param update_type: the type of the update
        '''
        parameters = {
            'action' : 'update',
            'device_serial_number' : self.device_serial_number,
            'update_type' : update_type,
            'version' : update_version
        }

        response = requests.get(
            self.update_url,  
            params=urllib.parse.urlencode(parameters)
            )

        if response.status_code == 422:
            Logger().log('Wrong parameters. Aborting update!')

        return response.json()['url']
    
    def __get_device_serial_number(self):
        '''
        Get the serial number of the device that the script runs on.
        Return default value of "0000000000000000" if the serial number is not in the "cpuinfo" file.
        '''

        serial = "0000000000000000"
        try:
            with open('/proc/cpuinfo','r') as cpuinfo_file:
                for line in cpuinfo_file:
                    if line[0:6]=='Serial':
                        serial = line[10:26]
        except:
            serial = "FAIL"

        return serial

    def restart_parent(self):
        '''
        Restart the parent process with the same arguments with which it was started.
        '''
        os.execl(sys.executable, *([sys.executable]+sys.argv))
    