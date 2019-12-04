from argparse import ArgumentParser
from security.crypto import Crypto

parser = ArgumentParser()
parser.add_argument('-C', '--conf', default="", type=str, help='configuration file')
parser.add_argument('-N', '--name', default="", type=str, help='user name')
parser.add_argument('-P', '--password', default="", type=str, help='user password')
args = parser.parse_args()
conf = args.conf
name = args.name
password = args.password

if (name != "" and password != "" and conf != ""):
    crypto = Crypto(conf)

    crypto.crypt([name, password])
else:
    exit