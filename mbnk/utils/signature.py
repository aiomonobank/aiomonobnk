__all__ = [
    'create_privkey_pubkey'
]

import base64
import ecdsa
import hashlib
import codecs


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
