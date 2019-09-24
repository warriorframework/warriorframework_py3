'''
Copyright 2017, Fujitsu Network Communications, Inc.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

"""This is utility for data encryption """

import os
import base64
import codecs
import traceback
import binascii

from warrior.Framework.Utils import file_Utils
from warrior.Framework.Utils.print_Utils import print_exception, print_error, print_warning
from warrior.Framework.Utils.testcase_Utils import pNote
from warrior import Tools

try:
    MOD = 'Pycryptodome'
    from Crypto.Cipher import AES
    from Crypto import Random
except ImportError as err:
    pNote("Please Install Pycryptodome 3.6.1 and above", "error")

def get_key(encoded_key):
    """
    Function that returns enc instance using
    secret key, passed to this
    function or read from secret.key file

    Args:
        encoded_key - False or base64 secrety key for encryption

    Return:
        IV - Random seed used to enc
        CIPHER - Enc instance used to for encryption
    """
    IV = None
    CIPHER = None
    MYFILE = Tools.__path__[0]+os.sep+"admin"+os.sep+'secret.key'
    try:
        if not encoded_key:
            with open(MYFILE, 'r') as myfileHandle:
                encoded_key = myfileHandle.read()
            if not encoded_key:
                raise IOError("encoded key is not present in secret.key file")
    except IOError:
        print_warning("Could not find the secret.key file in Tools/Admin! or secret.key is empty"
                      " use ./Warrior -encrypt anything -secretkey sixteenlenstring")
    else:
        try:
            IV = Random.new().read(AES.block_size)
            CIPHER = AES.new(base64.b64decode(encoded_key), AES.MODE_CFB, IV)
        except Exception as e:
            print_exception("Some problem occured: {0}".format(e))

    return IV, CIPHER


"""This is encryption"""
def encrypt(message, encoded_key=False):
    """This is encryption"""
    IV, CIPHER = get_key(encoded_key)
    msg = "Encrypted text could not be generated because the secret key in " \
          "the secret.key file seems to be incorrect."
    if IV is not None and CIPHER is not None:
        msg = IV + CIPHER.encrypt(message.encode('utf-8'))
        msg = codecs.encode(msg, "hex_codec")
    return str(msg, 'utf-8')

"""This is decryption"""
def decrypt(message, encoded_key=False):
    """This is decryption"""
    iv, cipher = get_key(encoded_key)
    if cipher is None:
        print_warning("encrypted messages if any, can't be decrypted")
        decrypt_message = message
    else:
        try:
            # in python2, can just use message.decode("hex")
            # but in python3, str.decode is removed
            decrypt_message = str(cipher.decrypt(codecs.decode(message, "hex_codec"))[len(iv):], 'utf-8')
        except binascii.Error as err:
            # This is dangerous...
            # using exception to handle if encrypted/not encrypted condition
            decrypt_message = message
        except Exception:
            decrypt_message = message
            print_error("Exception occured, couldn't decrypt given message")
            print_error(traceback.format_exc())
    return decrypt_message


def set_secret_key(plain_text_key):
    """
    Function that saves base64 encoded
    format of  secret key, passed to this
    function and saved to secret.key file

    Args:
        plain_text_key - Plain text key, that is is used for encryption

    Return:
        status - True if key is base64 encoded and saved
                 False if not saved
        key - base64 endoced key
    """
    encoded_key = False
    # Checks the length of the plain text secret key
    if not len(plain_text_key) == 16:
        print_error("The secret key needs to be exactly 16 characters in length"
                    ". {0} is {1} characters in length."
                    .format(plain_text_key, len(plain_text_key)))
        status = False
    else:
        # Gets base 64 encoding for the plain text secret key
        encoded_key = base64.b64encode(plain_text_key.encode('utf-8'))

        # Gets path to Tools
        path = Tools.__path__[0]

        # creates admin directory if that does not exist
        path = file_Utils.createDir(path, "admin")

        # creates secret.key file if it does not exists. Writes the base 64
        # encoded key to it.
        path = os.path.join(path, "secret.key")
        with open(path, 'w') as f:
            f.write(str(encoded_key, 'utf-8'))

        status = True
    return status, str(encoded_key, 'utf-8')
