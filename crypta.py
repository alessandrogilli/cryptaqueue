import base64
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
            # print(repr(plaintext.decode("utf-8"))) # Debug
            decoded = plaintext.decode("utf-8")
            result = "".join(
                [
                    x
                    for x in decoded
                    if x in string.printable and x not in ["\x0b", "\x0c", "\n"]
                ]
            )
            return result
        except:
            return None

    def string2hash(self, string):
        return base64.b64encode(SHA256.new(string.encode()).digest()).decode()
