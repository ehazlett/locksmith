import hashlib
from Crypto.Cipher import AES
from django.utils.translation import ugettext as _
import base64
from django.conf import settings

def hash_text(text):
    """
    Hashes text with app key

    :param text: Text to encrypt

    """
    h = hashlib.sha256()
    h.update(getattr(settings, 'SECRET_KEY'))
    h.update(text)
    return h.hexdigest()

def _get_padded_key(key=None):
    if len(key) < 16:
        pad = 16 - len(key)
        k = key + ('^'*pad)
    else:
        k = key[:16]
    return k

def encrypt(data=None, key=None):
    """
    Encrypts data

    :param data: Data to encrypt
    :param key: Encryption key (salt)

    """
    k = _get_padded_key(key)
    e = AES.new(k, AES.MODE_CFB, k[::-1])
    enc = e.encrypt(data)
    return base64.b64encode(enc)

def decrypt(data=None, key=None):
    """
    Decrypts data

    :param data: Encrypted data to decrypt
    :param key: Encryption key (salt)

    """
    k = _get_padded_key(key)
    e = AES.new(k, AES.MODE_CFB, k[::-1])
    dec = e.decrypt(base64.b64decode(data))
    try:
        unicode(dec)
    except:
        dec = ''
    return dec
