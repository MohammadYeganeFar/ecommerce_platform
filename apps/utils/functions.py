"""
purpose:
1- creating different types of functions(not classes),
with varios purposes like encrypting, logging

"""
from hashlib import sha256
import time
import secrets
import string
from setting import DIRS
# a func for encrypt the text and return that
def encrypter(text : str) :
    return  sha256(text.encode("utf-8")).hexdigest()



def generate_random_code(length=8):
    """Generates a secure random code of specified length with letters and digits."""
    characters = string.ascii_letters + string.digits
    random_code = ''.join(secrets.choice(characters) for _ in range(length))
    return random_code






































