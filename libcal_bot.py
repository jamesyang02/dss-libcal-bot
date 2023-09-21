from selenium import webdriver # Selenium takes control of the web browser
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager # webdriver_manager is a package that helps you to download and open the browser driver automatically.
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

"""
LibCal Room Booking Bot Developed by
DSS Tech Committee Fall 2023
========================================
This bot is designed to automate the process of booking a room in any library on campus.
"""
# Initialize the webdriver
options = webdriver.ChromeOptions()
# get rid of the ugly certificate warnings from Selenium
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("ignore-certificate-errors")

# SO NO HEAD???? (gets rid of visible chrome window)
options.add_argument("--headless=new") # makes it faster, but you won't see what's happening

options.add_experimental_option("detach", True) 
service = Service(ChromeDriverManager().install()) # installs the chrome that this webdriver will use
driver = webdriver.Chrome(options=options, service=service) # start up the webdriver
wait = WebDriverWait(driver, 3)

# Open the website
driver.get("https://berkeley.libcal.com/")

# PSEUDOCODE!!!
