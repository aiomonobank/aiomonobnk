__all__ = [
    'webhook_authentication'
]

import base64
import hashlib

import ecdsa


def webhook_authentication(pub_key_base64: str, x_sign_base64: str, body_bytes: bytes) -> bool:
    pub_key_bytes = base64.b64decode(pub_key_base64)
    signature_bytes = base64.b64decode(x_sign_base64)
    pub_key = ecdsa.VerifyingKey.from_pem(pub_key_bytes.decode())

    if pub_key.verify(signature_bytes, body_bytes, sigdecode=ecdsa.util.sigdecode_der, hashfunc=hashlib.sha256):
        return True

    return False
