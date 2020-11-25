import os
import subprocess

class Releaser():
    def __init__(self):
        pass
    
    def clear_deployment_bucket(self):
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

    def build_release_archive(self):
        print('>>> Building release archive.')

    def release(self):
        print('>>> Releasing new version.')

    def __get_latest_version(self):
        print('>>> Retrieving latest release version.')
    
    def __build_new_version(self):
        print('>>> Building new release version.')


def main():
    releaser = Releaser()
    
    release_flow = [
        releaser.clear_deployment_bucket,
        releaser.build_release_archive,

    ]

    

main()