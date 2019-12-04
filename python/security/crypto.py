from cryptography.fernet import Fernet
from argparse import ArgumentParser
import hashlib, random, string, os

class Crypto():

    def __init__(self, folder):
        if (folder == ""):
            raise Exception("Folder is empty")

        self.folder = folder
        self.key_hash = b'ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg='
        self.cipher_suite = Fernet(self.key_hash)

    def crypt(self, fields):
        encrypted_fields = []
        for field in fields:
            encrypted_fields.append(self.cipher_suite.encrypt(field.encode('utf-8')))

        encrypted_fields = [encrypted.decode('utf-8') for encrypted in encrypted_fields]

        with open(self.folder, 'w+') as config:
            config.write('\n'.join(encrypted_fields))

    def decrypt(self):
        if (os.path.isfile(self.folder)):
            with open(self.folder, 'r+') as config:
                results = []
                for line in config.readlines():
                    results.append(self.cipher_suite.decrypt(line.encode('utf-8')))

            results = [decrypted.decode('utf-8') for decrypted in results]
        else:
            results = []
            
        return results
