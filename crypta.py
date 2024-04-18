import base64
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

class Crypta:

    def __init__(self) -> None:
        import os
        from dotenv import load_dotenv
        load_dotenv()

        self.IV = base64.b64decode(os.getenv('B64_IV'))
        self.PASSWORD = os.getenv('PASSWORD')

    def encrypt(self, plaintext: str) -> bytes:
        # Padding PKCS#7
        plaintext = plaintext.encode()
        length = 16 - (len(plaintext) % 16)
        plaintext += bytes([length])*length
        # Encryption
        aes = AES.new(SHA256.new(str.encode(self.PASSWORD)).digest(), AES.MODE_CBC, self.IV)
        return aes.encrypt(plaintext)

    def decrypt(self, ciphertext) -> bytes | None:
        try:
            aes = AES.new(SHA256.new(str.encode(self.PASSWORD)).digest(), AES.MODE_CBC, self.IV)    
            return aes.decrypt(ciphertext)
        except:
            return None

    def try_decrypt(self, ciphertext) -> str | None:

        plaintext = self.decrypt(ciphertext)
        try:
            result = plaintext.decode('utf8').rstrip("\x0c").rstrip("\n")
            return result
        except:
            return None
        
    def string2hash(self, string):
        return base64.b64encode(SHA256.new(string.encode()).digest()).decode()
        