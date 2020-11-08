import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES 
from login import models
import os
from datetime import datetime

keys = os.environ.get('OAUTHKEYS') #OAUTHKEYS
expired_time_sec = os.environ.get('OAUTHEXP')

def check_active_cookie(request):
    if request.COOKIES.get('user_info') is not None:
        en = AESCipher()
        decrypt_data = en.decrypt(request.COOKIES.get('user_info').encode("UTF-8"))
        arr = decrypt_data.split('&')

        # read access token from db
        q_set = models.Oauth42.objects.get(login=arr[0])

        # verify access token and session cookie value
        if datetime.now().timestamp() - q_set.created_at.timestamp() < int(expired_time_sec) and q_set.access_token == arr[1]:
            return 0
        else:
            return -1
    else:
        return -1

def get_active_cookie(request, login:str, token:str):
    try:
        en = AESCipher()
        secret_value = en.encrypt(login+'&'+token)

        db = models.Oauth42(login=login, access_token=token)
        db.save()

        return secret_value
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


