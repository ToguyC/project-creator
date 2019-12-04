import os, sys, time
from argparse import ArgumentParser
from selenium import webdriver
from security.crypto import Crypto

parser = ArgumentParser()
parser.add_argument('-p', '--project', default="python", type=str, help='project name')
parser.add_argument('-F', '--folder', default="", type=str, help='project name')
args = parser.parse_args()
project = args.project
folder = args.folder
driver = folder + "driver"
conf = folder + "user.conf"

browser = webdriver.Firefox(executable_path=driver + "\\geckodriver.exe")
browser.get('http://github.com/login')

crypto = Crypto(conf)

def createRepo():
    user_infos = crypto.decrypt()

    # Login
    python_action = browser.find_element_by_xpath("//*[@id='login_field']")
    python_action.send_keys(user_infos[0])
    with open(folder + "output.txt", 'w+') as temp:
        temp.write(user_infos[0])
    python_action = browser.find_element_by_xpath("//*[@id='password']")
    python_action.send_keys(user_infos[1])
    python_action = browser.find_element_by_xpath("/html/body/div[3]/main/div/form/div[3]/input[8]")
    python_action.click()

    # New repo
    python_action = browser.find_element_by_xpath("/html/body/div[1]/header/div[6]/details")
    python_action.click()
    python_action = browser.find_element_by_xpath("/html/body/div[1]/header/div[6]/details/details-menu/a[1]")
    python_action.click()

    # Create repo
    python_action = browser.find_element_by_xpath("//*[@id='repository_name']")
    python_action.send_keys(project)
    time.sleep(0.5)
    python_action = browser.find_element_by_css_selector("button.first-in-line")
    python_action.submit()

    # Close
    browser.close()

if __name__ == "__main__":
    createRepo()