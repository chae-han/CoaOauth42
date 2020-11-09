import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES 
from login import models
import os
from datetime import datetime

keys = os.environ.get('OAUTHKEYS')
expired_time_sec = int(os.environ.get('OAUTHEXP'))


def set_cookie(response, cookies:dict):
    for key, value in cookies.items():
        # set_cookie(key, value='', max_age=None, expires=None, path='/', domain=None, secure=None, httponly=False, samesite=None) :
        response.set_cookie(key, value, max_age=expired_time_sec)
    return response

def del_cookie(response):
    pass

def check_active_cookie(request):
    try:
        if request.COOKIES.get('usif') is not None:
            en = AESCipher()
            decrypt_data = en.decrypt(request.COOKIES.get('usif').encode("UTF-8"))
            arr = decrypt_data.split('&')

            # read access token from db
            q_set = models.Oauth42.objects.filter(login=arr[0])

            # verify access token and session cookie value
            if q_set.exists() and datetime.now().timestamp() - q_set.values()[0]['created_at'].timestamp() < expired_time_sec and q_set.values()[0]['access_token'] == arr[1]:
                return arr[0] # return login
        return -1
    except Exception as e:
        print(e)
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


