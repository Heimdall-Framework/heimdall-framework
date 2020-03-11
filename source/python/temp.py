import os
import json
import sys


with open(os.path.join(sys.path[0], 'config.json')) as config_file:
    ext = json.load(config_file)
    print(ext[0]['name'])