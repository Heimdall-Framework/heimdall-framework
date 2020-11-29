import os
import re
import sys
import json
import requests
import subprocess

class Releaser():
    def __init__(self):
        pass
    
    def clear_deployment_bucket(self) -> bool:
        """
        Clears the AWS S3 deployment bucket of the core framework.
        """
        print('>>> Clearing deployment bucket.')
        
        deployment_bucket = os.environ['DEPLOYMENT_BUCKET']
        clear_command = 'aws s3 rm {} --recursive --exclude="*" --include="*.tar.gz"'.format(deployment_bucket)

        try:
            subprocess.check_call(clear_command.split())
        except subprocess.CalledProcessError as command_error:
            print('>>> Bucket clearing failed.')
            print('>>> {}'.format(command_error))
            
            return False
        return True

    def release(self) -> (str, bool):
        """
        Releases the current framework version.
        """        
        print('>>> Releasing new version.')
        
        latest_release_version, retrieval_result = self.__get_latest_version()
        if not retrieval_result:
            print('>>> Failure to retrieve latest release version broke the release procedure.')
            return '', False

        release_level, retrieval_result = self.__get_release_level()
        if not retrieval_result:
            print('>>> Failure to retrieve release commit message broke the release procedure.')
            return False

        if release_level == '':
            release_level = 'patch'

        new_version, building_result = self.__build_new_version(release_level, latest_release_version)
        if not building_result:
            print('>>> Failure to build new version broke the release procedure.')
            return False

        if not self.__build_release_archive(new_version):
            print ('>>  Failure to build release archive broke the release procedure.')
            return False

        if not self.__upload_new_release():
            print('>>> Failure to upload new release broke the release procedure.')
            return False

        if not self.__update_latest_version(latest_release_version, new_version):
            print('>>> Failure to upload new release broke the release procedure.')
            print('>>> Check the release versions immediately!')
            return False
        
        return True

    def __upload_new_release(self) -> bool:
        print('>>> Uploading new release version.')

        deployment_bucket = os.environ['DEPLOYMENT_BUCKET']
        sync_command = 'aws s3 sync source/releaser/release/ {}'.format(deployment_bucket)

        try:
            subprocess.check_call(sync_command.split())
        except subprocess.CalledProcessError as command_error:
            if command_error.returncode == 1:
                return True

            print('>>> Syncing to S3 failed.')
            print('>>> {}'.format(command_error))
            
            return False
        return True

    def __build_release_archive(self, version) -> bool:
        print('>>> Building release archive.')
        dir_path = os.path.dirname(os.path.realpath(__file__))
        build_tar_command = 'tar -czf {}/release/core-{}.tar.gz {}/../../../repo'.format(dir_path, version, dir_path)

        try:
            subprocess.check_call(build_tar_command.split())
        except subprocess.CalledProcessError as command_error:
            if command_error.returncode == 1:
                return True

            print('>>> Release archive creating failed.')
            print('>>> {}'.format(command_error))
            
            return False
        return True


    def __get_release_level(self) -> (str, bool):
        print('>>> Retrieving current release level.')
        get_release_level_command = 'git log --oneline -1 --pretty=%B'
        release_message = ''
        release_level = ''

        try:
            release_message = subprocess.check_output(get_release_level_command.split()).decode('utf-8').replace('\n', '')
        except subprocess.CalledProcessError as command_error:
            print('>>> Failed to retrieve release commit message.')
            print('>>> {}'.format(command_error))
            
            return '', False
        
        release_level = re.search(r'\[(.*?)\]', release_message)
        
        if release_level == None:
            return '', True

        return release_level.group(1).lower(), True

    def __get_latest_version(self):
        print('>>> Retrieving latest release version.')

        versioning_controller_get_url = os.environ['VERSIONING_CONTROLLER_GET_URL']
        
        request_result = requests.get(versioning_controller_get_url)
        request_body = request_result.json()

        if not 'version' in request_body:
            print('>>> Failed to retrieve latest version.')
            return '', False

        return request_body['version'], True

    
    def __build_new_version(self, release_level, latest_release_version) -> (str, bool):
        print('>>> Building new release version.')
        new_release_version = ''

        if release_level == 'major':
            new_release_version = '{}.{}.{}'.format(
                str(int(latest_release_version.split('.')[0]) + 1),
                 '0',
                 '0'
                )
        elif release_level == 'minor':
            new_release_version = '{}.{}.{}'.format(
                latest_release_version.split('.')[0],
                str(int(latest_release_version.split('.')[1]) + 1),
                '0'
            )
        elif release_level == 'patch':
            new_release_version = '{}.{}.{}'.format(
                latest_release_version.split('.')[0],
                latest_release_version.split('.')[1],
                str(int(latest_release_version.split('.')[2]) + 1)
            )
        else:
            print('>>> Something went terribly wrong while checking release level!')
            return '', False

        return new_release_version, True

    def __update_latest_version(self, old_version, new_version) -> bool:
        ci_secret = os.environ['CI_SECRET_KEY']
        update_version_service_url = os.environ['VERSIONING_CONTROLLER_UPDATE_URL'] 

        body = {
            'ci_secret': ci_secret,
            'old_version': old_version,
            'new_version': new_version
        }

        request_result = requests.post(update_version_service_url, data = json.dumps(body))
        return request_result.status_code == 200


def main():
    releaser = Releaser()
    
    release_flow = [
        releaser.clear_deployment_bucket,
        releaser.release
    ]

    for release_operation in release_flow:
        if not release_operation():
            print('!>>> RELEASE FAILED <<<!')
            sys.exit(1)

    print('>>> Release was SUCCESSFUL.')

main()