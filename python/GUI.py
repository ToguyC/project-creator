from cryptography.fernet import Fernet
from argparse import ArgumentParser
import hashlib, random, string

parser = ArgumentParser()
parser.add_argument('-F', '--folder', default="", type=str, help='project name')
args = parser.parse_args()
folder = args.folder

if (folder == ""):
    exit()

key_hash = b'ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg='
cipher_suite = Fernet(key_hash)

def crypt():
    user = input('Enter username: ').encode('utf-8')
    password = input('Enter password: ').encode('utf-8')

    user_crypt = cipher_suite.encrypt(user)
    password_crypt = cipher_suite.encrypt(password)

    with open(folder, 'w+') as config:
        config.write('\n'.join([user_crypt.decode('utf-8'), password_crypt.decode('utf-8')]))

def decrypt():
    with open(folder, 'r+') as config:
        user_decrypt = cipher_suite.decrypt(config.readlines()[0].encode('utf-8'))
        password_decrypt = cipher_suite.decrypt(config.readlines()[1].encode('utf-8'))

    return [user_decrypt, password_decrypt]

decrypt()