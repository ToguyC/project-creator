from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-F', '--folder', default="python", type=str, help='project name')
parser.add_argument('-C', '--conf', default="python", type=str, help='project name')
args = parser.parse_args()
folder = args.folder
conf = args.conf

with open(conf, 'w+') as file:
    file.write(folder)