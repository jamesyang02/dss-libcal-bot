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
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("ignore-certificate-errors")
options.add_argument("--headless=new")
options.add_experimental_option("detach", True)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(options=options, service=service)
wait = WebDriverWait(driver, 10)  # Increased the timeout to 10 seconds

# Open the website
driver.get("https://berkeley.libcal.com/")

# Function to read user input from a text file
def read_user_input(file_path):
    user_input = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split(': ')
            user_input[key] = value
    return user_input

# Read user input from the text file
user_input = read_user_input("user_input.txt")

# Extract library_name, date, and start_times from user_input
library_name = user_input.get("Library")
date = user_input.get("Date")
start_times_str = user_input.get("Start Times")
# Convert start_times_str to a list of start times
start_times = [time.strip() for time in start_times_str.split(',')]

# Define functions for interacting with the website
def select_library(library_name):
    # Locate and click on the library selection element
    library_select = driver.find_element(By.XPATH, "//your-library-xpath")
    library_select.click()

def select_date(date):
    # Locate and interact with the date selection element
    date_input = driver.find_element(By.XPATH, "//your-date-input-xpath")
    date_input.clear()
    date_input.send_keys(date)
    date_input.send_keys(Keys.RETURN)

def select_time_slots(start_times):
    # Locate and select time slots based on start times
    for start_time in start_times:
        time_slot_xpath = f"//your-time-slot-xpath[contains(text(), '{start_time}')]"
        time_slot = wait.until(EC.element_to_be_clickable((By.XPATH, time_slot_xpath)))
        time_slot.click()

def submit_booking():
    # Locate and click on the "Submit Times" button
    submit_button = driver.find_element(By.XPATH, "//your-submit-button-xpath")
    submit_button.click()

select_library(library_name)
select_date(date)
select_time_slots(start_times)
submit_booking()
