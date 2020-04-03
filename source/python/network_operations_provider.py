import json
from logger import Logger
import urllib
import urllib.request
from collections import namedtuple

class NetworkOperationsProvider():

    # gets the checksum of the leatest Tails distribution iso, returns null if internet connection is not present
    def get_tails_checksum(self):
        try:
            with urllib.request.urlopen("https://tails.boum.org/install/v2/Tails/amd64/stable/latest.json") as url:
                received_data = json.loads(url.read().decode())

                mirror_one_hash = received_data['installations'][0]['installation-paths'][0]['target-files'][0]['sha256']
                mirror_two_hash = received_data['installations'][0]['installation-paths'][1]['target-files'][0]['sha256']
            
                return mirror_one_hash, mirror_two_hash
        except:
            Logger().log('> No internet connection.')
            return None, None
