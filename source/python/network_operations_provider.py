import json
import urllib.request as requester
from collections import namedtuple

class NetworkOperationsProvider():
    def get_tails_checksum(self):
        with requester.urlopen("https://tails.boum.org/install/v2/Tails/amd64/stable/latest.json") as url:
            received_data = json.loads(url.read().decode())

            list(received_data['installations'][0].values())[0][0]
            return True