from cryptography.fernet import Fernet
import base64


# we will be encrypting the below string.
def encryption(message, key):
    key = key.encode()
    key64 = base64.b64encode(key)

    # Instance the Fernet class with the key
    fernet = Fernet(key64)

    # then use the Fernet class instance
    # to encrypt the string must
    # be encoded to byte string before encryption
    encmessage = fernet.encrypt(message.encode())
    return encmessage.decode()


def decryption(encmessage, key):
    key = key.encode()
    key64 = base64.b64encode(key)

    # Instance the Fernet class with the key
    fernet = Fernet(key64)

    # then use the Fernet class instance
    # to encrypt the string string must
    # be encoded to byte string before encryption
    decmessage = fernet.decrypt(encmessage)
    return decmessage
