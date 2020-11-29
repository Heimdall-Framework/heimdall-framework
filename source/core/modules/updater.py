import os
import sys
import json
import shutil
import tarfile
import urllib
import requests
from datetime import datetime
from .logger import Logger
from .framework_configuration import FrameworkConfiguration
from .system_operations_provider import SystemOperationsProvider

TEMP_DIR_NAME = '/tmp/temp_update_data/'

class Updater():
    def __init__(self,configuration: FrameworkConfiguration, logger: Logger, framework_location: str, update_url: str):
        self.__configuration = configuration
        self.__logger = logger
        self.__framework_location = framework_location
        self.__framework_parent_directory = framework_location + '/../'
        self.__version_logs_location = framework_location + '/source/core/python/update_logs/versions.json'
        self.__plugins_directory_location = framework_location + '/source/core/python/plugins/'
        self.__last_update_file_location = framework_location + '/source/core/python/update_logs/last_update_date.log'


        self.update_url = update_url

    def update(self, logger) -> None:
        '''
        Update the running version of the framework or it's plugins if newer ones exist.
        Return True or False, depending on the outcome of the operation.
        '''
        
        try:
            is_new = True
            self.device_serial_number = self.__get_device_serial_number()

            if self.device_serial_number == 'FAIL':
                self.__logger.log('>>> Device serial number cannot be retrieved.')
                return False
            
            self.__load_update_logs()
            self.__load_plugins_config()

            available_updates = self.__get_available_updates()
            
            if available_updates == None:
                self.__logger.log('>>> No available updates were loaded.')
                return False

            for update in available_updates:
                if update['name'] == 'none':
                    self.__logger.log('>>> The update repository is currently empty. Update is being skipped.')
                    return False
                    
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

            with open(self.__version_logs_location, 'w') as update_logs_file:
                update_logs_file.write(json.dumps(self.update_logs))
            
            SystemOperationsProvider().rebuild_package(self.__framework_location)
            return True

        except Exception as exception:
            self.__logger.log('>>> Updating procedure failed. Excpetion: ' + str(exception))
            return False

    def can_update(self, logger):
        '''
        Check if any new updates are available.
        '''

        current_file_directory = os.path.dirname(os.path.abspath(__file__))
        self.core_framework_location = os.path.abspath(os.path.join(current_file_directory, '../../../../'))

        if not os.path.isfile(self.__last_update_file_location):
            with open(self.__last_update_file_location, 'w'):
                logger.log('>>> Created an empty last_updated.log')
            
        if not os.path.isfile(self.__version_logs_location):
            with open(self.__version_logs_location, 'w'):
                logger.log('>>> Created an empty versions.json')

        with open(self.__last_update_file_location) as last_update_date:
            last_update_date =  last_update_date.read()
        
        if self.__configuration.updates_intensity == 'normal':
            if not (last_update_date == '' or last_update_date != datetime.now().strftime('%b %d %Y')):
                logger.log('>>> Update date is not reached yet.')
                return False

        return True
            

    def __load_update_logs(self) -> None:
        '''
        Loads the update logs file into a list.
        '''

        with open(self.__version_logs_location, 'r') as update_logs_file:
            self.update_logs = json.loads(update_logs_file.read() or '[]')

    def __load_plugins_config(self) -> None:
        with open(self.__plugins_directory_location + '/config.json') as plugins_config:
            self.plugins_config = json.loads(plugins_config.read() or '[]')

    def __get_available_updates(self) -> str:
        '''
        Get all available updates from a remote host.
        '''
        
        parameters = {
            'action' : 'info',
            'device_serial_number' : self.device_serial_number
        }

        response = requests.get(
            self.update_url, 
            params=urllib.parse.urlencode(parameters)
            )

        if response.status_code == 422:
            self.__logger.log('>>> Wrong parameters. Aborting update!')
            return None
        elif response.status_code == 502:
            self.__logger.log('>>> Internal server error. Aborting update!')
            return None

        return response.json()

    def __process_update(self, download_url: str, is_plugin: bool) -> bool:
        '''
        Download, decompress and install a given update.
        
        :param download_url: the temporary link from which the update can be downloaded
        :param is_plugin: a boolean that indicates whether the update is plugin or the core framework
        '''

        try:
            if not os.path.isdir(TEMP_DIR_NAME):
                os.mkdir(TEMP_DIR_NAME)

            urllib.request.urlretrieve(download_url, TEMP_DIR_NAME + '/update.tar.gz')

            archive = tarfile.open(TEMP_DIR_NAME + '/update.tar.gz', "r:gz")
            archive.extractall(TEMP_DIR_NAME)
            archive.close()

            for root, dirs, files in os.walk(TEMP_DIR_NAME):
                if is_plugin:
                    plugin_files = self.__get_python_plugin_files(files)

                    for file in plugin_files:
                        shutil.copy(
                            file, 
                            self.__plugins_directory_location
                            )
                    break
                else:
                    if 'heimdall-framework' in root:
                        for file in files:
                            shutil.copy(
                                root + '/' + file, 
                                root.replace(TEMP_DIR_NAME + 'heimdall-framework', self.__framework_location) + '/' + file
                                )
            
            shutil.rmtree(TEMP_DIR_NAME)
            return True

        except Exception as exception:
            shutil.rmtree(TEMP_DIR_NAME)
            self.__logger.log('>>> Processing update failed. Excpetion: ' + str(exception))
            return False

    def __update_plugins_config(self, plugin_name: str) -> None:
        '''
        Update the plugin configuration list.
        
        :param plugin_name: the name of the plugin
        '''
        
        self.plugins_config.append({
            'name' : plugin_name,
            'main_function' : 'main',
            'enabled' : True
        })

    def __get_python_plugin_files(self, files: str) -> list:
        '''
        Get all plugin files from a temporary directory.

        :param files: a list of the names of all files in a directory
        '''
        
        python_files = list()

        for file_name in files:
            if file_name.endswith('.py') or file_name.endswith('.pyc'):
                python_files.append(TEMP_DIR_NAME + file_name)

        return python_files

    def __get_download_link(self, update_name: str, update_version: str, update_type: str) -> str:
        '''
        Get the download link for the update.

        :param update_name: the name of the update
        :param update_version: the version of the update
        :param update_type: the type of the update
        '''

        version = '{}-{}'.format(update_name, update_version)

        parameters = {
            'action' : 'update',
            'device_serial_number' : self.device_serial_number,
            'update_type' : update_type,
            'version' : version
        }

        response = requests.get(
            self.update_url,  
            params=urllib.parse.urlencode(parameters)
            )

        if response.status_code == 422:
            self.__logger.log('Wrong parameters. Aborting update!')

        return response.json()['url']
    
    def __get_device_serial_number(self) -> str:
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

    def restart_parent(self) -> None:
        '''
        Restart the parent process with the same arguments with which it was started.
        '''
        os.execl(sys.executable, *([sys.executable]+sys.argv))
    