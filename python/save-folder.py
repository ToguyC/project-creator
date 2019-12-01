from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-F', '--folder', default="python", type=str, help='project name')
args = parser.parse_args()
folder = args.folder

with open("E:\\Programmation\\Utilities\\project-creator\\user-folder.conf", 'w+') as file:
    file.write(folder)