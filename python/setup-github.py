import os, sys
from argparse import ArgumentParser
from selenium import webdriver

parser = ArgumentParser()
parser.add_argument('-p', '--project', default="python", type=str, help='project name')
parser.add_argument('-u', '--user', default=None, type=str, help='github user')
parser.add_argument('-P', '--password', default=None, type=str, help='user password')
args = parser.parse_args()
project = args.project
user = args.user
password = args.password

browser = webdriver.Firefox(executable_path="C:\\Users\\cavagnat\\Documents\\Programmation\\Utilities\\project-creator\\driver\\geckodriver.exe")  # Optional argument, if not specified will search path.
browser.get('http://github.com/login');

def createRepo():
    # Login
    python_action = browser.find_element_by_xpath("//*[@id='login_field']")
    python_action.send_keys(user)
    python_action = browser.find_element_by_xpath("//*[@id='password']")
    python_action.send_keys(password)
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
    python_action = browser.find_element_by_css_selector("button.first-in-line")
    python_action.submit()

    # Close
    browser.close()

if __name__ == "__main__":
    createRepo()