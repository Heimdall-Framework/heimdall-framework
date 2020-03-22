import json
from logger import Logger
import urllib
from collections import namedtuple

class NetworkOperationsProvider():

    # gets the checksum of the leatest Tails distribution iso
    def get_tails_checksum(self):
        try:
            with urllib.request.urlopen("https://tails.boum.org/install/v2/Tails/amd64/stable/latest.json") as url:
                received_data = json.loads(url.read().decode())

                return list(received_data['installations'][0].values())[0][0]
        except:
            Logger().log('> No internet connection.')
            return None
            