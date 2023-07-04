__all__ = [
    'create_privkey_pubkey'
]

import base64
import ecdsa
import hashlib
import codecs

from typing import List
from datetime import datetime


def generate_sign(privkey_path: str, timestamp: str, url: str):
    data = (timestamp + url).encode('utf-8')

    with codecs.open(privkey_path, 'r', 'utf-8') as f:
        privkey = f.read()
        f.close()

    private_key = ecdsa.SigningKey.from_pem(privkey, hashfunc=hashlib.sha256)

    sign = private_key.sign(data, hashfunc=hashlib.sha256)
    sign_base64 = base64.b64encode(sign)

    return sign_base64


def create_privkey_pubkey(privkey_path: str, pubkey_path: str):
    private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1, hashfunc=hashlib.sha256)
    public_key = private_key.get_verifying_key()

    privkey = private_key.to_pem()
    pubkey = public_key.to_pem()

    with codecs.open(privkey_path, 'w', 'utf-8') as f:
        f.write(privkey.decode('utf-8'))
        f.close()

    with codecs.open(pubkey_path, 'w', 'utf-8') as f:
        f.write(pubkey.decode('utf-8'))
        f.close()
