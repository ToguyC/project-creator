import os, sys
from bs4 import BeautifulSoup as Soup
from argparse import ArgumentParser
from selenium import webdriver

parser = ArgumentParser()
parser.add_argument('-p', '--project', default="python", type=str, help='port to listen on')
args = parser.parse_args()
project = args.project

browser = webdriver.Firefox(executable_path="E:\\Programmation\\Utilities\\project-creator\\driver\\geckodriver.exe")  # Optional argument, if not specified will search path.
browser.get('http://github.com/login');

def createRepo():
    # Login
    python_action = browser.find_element_by_xpath("//*[@id='login_field']")
    python_action.send_keys('tanguy.cvgn@eduge.ch')
    python_action = browser.find_element_by_xpath("//*[@id='password']")
    python_action.send_keys('~"^4x&aVKx8j')
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