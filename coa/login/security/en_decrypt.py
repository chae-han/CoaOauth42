# from aescipher import *

# key = [0x10, 0x01, 0x15, 0x1B, 0xA1, 0x11, 0x57, 0x72, 0x6C, 0x21, 0x56, 0x57, 0x62, 0x16, 0x05, 0x3D,
#         0xFF, 0xFE, 0x11, 0x1B, 0x21, 0x31, 0x57, 0x72, 0x6B, 0x21, 0xA6, 0xA7, 0x6E, 0xE6, 0xE5, 0x3F]
# from pycryptodome import *
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES 
from login import models



def had_active_cookie(request):

    if request.session.get('user_info', False):
        en = AESCipher()
        decrypt_data = en.decrypt(request.session['user_info'])
        arr = decrypt_data.split('&')
        print(arr)

        # read access token from db
        access_token = models.Oauth42.objects.filter(login=arr[0])

        # verify access token and session cookie value
        if access_token == arr[1]:
            return 0
        else:
            return -1
    else:
        return -1

def set_active_cookie(request, login:str, token:str):
    try:
        en = AESCipher()
        secret_value = en.encrypt(login+'&'+token)

        request.session['user_info'] = secret_value
        db = models.Oauth42(login=login, access_token=token)
        db.save()

        return 0
    except:
        return -1


class AESCipher():

    #def __init__(self, key):
    def __init__(self): #
        self.bs = 32
        self.key = hashlib.sha256(AESCipher.str_to_bytes(keys)).digest()

    @staticmethod
    def str_to_bytes(data):
        u_type = type(b''.decode('utf8'))
        if isinstance(data, u_type):
            return data.encode('utf8')
        return data

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * AESCipher.str_to_bytes(chr(self.bs - len(s) % self.bs))

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

    def encrypt(self, raw):
        raw = self._pad(AESCipher.str_to_bytes(raw))
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw)).decode('utf-8')

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')


