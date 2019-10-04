import string
import random


class DataProvider:

    def generate_pseudorandom_string(self, length=32):
        characters_set =string.ascii_letters + string.digits

        pseudorandom_string = ''.join(random.choice(characters_set) for i in range(length))

        return pseudorandom_string
