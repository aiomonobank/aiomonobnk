__all__ = [
    'create_secrets'
]

import ecdsa
import hashlib
import codecs


def create_secrets(privkey_path: str, pubkey_path: str) -> None:
    private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1, hashfunc=hashlib.sha256)
    public_key = private_key.get_verifying_key()

    private_key_pem = private_key.to_pem()
    public_key_pem = public_key.to_pem()

    with codecs.open(privkey_path, 'w', 'utf-8') as f:
        f.write(private_key_pem.decode('utf-8'))

    with codecs.open(pubkey_path, 'w', 'utf-8') as f:
        f.write(public_key_pem.decode('utf-8'))
