import hashlib
from Crypto.Cipher import AES
from django.utils.translation import ugettext as _
import base64
from django.conf import settings
from django.core.cache import cache
from django.contrib.auth.models import User
import string
import random

def generate_password(length=16):
    """
    Generates a new random password
    
    :param length: Length of password

    """
    return ''.join(random.sample(string.letters+string.digits, length))

def set_user_encryption_key(username=None, key=None, ttl=None):
    """
    Sets the encryption key for the specified user

    """
    if not ttl:
        u = User.objects.get(username=username)
        ttl = u.get_profile().encryption_key_timeout
    cache.set(settings.CACHE_ENCRYPTION_KEY.format(username), key,
        timeout=ttl)

def get_user_encryption_key(username=None):
    """
    Gets the encryption key for the specified user

    """
    return cache.get(settings.CACHE_ENCRYPTION_KEY.format(username))

def clear_user_encryption_key(username=None):
    """
    Clears the encryption key for the specified user

    """
    cache.delete(settings.CACHE_ENCRYPTION_KEY.format(username))

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
