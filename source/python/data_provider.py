import string
import random
from logger import log

class DataProvider:
    def generate_random_data_file(self):
        try:
            file_content = self.__generate_pseudorandom_string(128)
            file = open('dump.me', 'w')
            file.write(file_content)
            
            return True
        except:
            log('> File creation exception.')
            return False


    def __generate_pseudorandom_string(self, length=32):
        characters_set =string.ascii_letters + string.digits
        pseudorandom_string = ''.join(random.choice(characters_set) for i in range(length))

        return pseudorandom_string