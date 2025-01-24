import base64
import json
import string

from Crypto.Cipher import AES
from Crypto.Hash import SHA256


class Crypta:
    def __init__(self) -> None:
        import os

        from dotenv import load_dotenv

        load_dotenv()

        self.IV = base64.b64decode(os.getenv("B64_IV"))
        self.PASSWORD = os.getenv("PASSWORD")

    def encrypt(self, plaintext: str) -> bytes:
        """
        b64(AES(plaintext))
        """
        # Padding PKCS#7
        plaintext = plaintext.encode()
        length = 16 - (len(plaintext) % 16)
        plaintext += bytes([length]) * length
        # Encryption
        aes = AES.new(
            SHA256.new(str.encode(self.PASSWORD)).digest(), AES.MODE_CBC, self.IV
        )
        return base64.b64encode(aes.encrypt(plaintext))

    def decrypt(self, ciphertext) -> bytes | None:
        """
        AES_d(b64_d(ciphertext))
        """
        try:
            aes = AES.new(
                SHA256.new(str.encode(self.PASSWORD)).digest(), AES.MODE_CBC, self.IV
            )
            return aes.decrypt(base64.b64decode(ciphertext))
        except:
            return None

    def try_decrypt(self, ciphertext) -> str | None:
        try:
            plaintext = self.decrypt(ciphertext)
            decoded = plaintext.decode("utf-8")
            decoded = "".join(
                [
                    x
                    for x in decoded
                    if x in string.printable[:-5]  # Excludes \t, \n, \r, \x0b, \x0c
                ]
            )
            d = json.loads(decoded)
            return d
        except:
            return None
