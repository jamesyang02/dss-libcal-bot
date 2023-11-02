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
    # Define a dictionary to map library names to their corresponding XPath expressions
    library_xpath_mapping = {
        "Earth Sciences & Map Seminar Room": '//*[@id="s-lc-content-eqlist-67826"]/div/ul[1]/li/a',
        "East Asian Library Study Rooms": '//*[@id="s-lc-content-eqlist-67826"]/div/ul[2]/li/a',
        "Environmental Design Library Group Study Room": '//*[@id="s-lc-content-eqlist-67826"]/div/ul[3]/li/a',
        "IGS Library (Matsui Center) Study Room": '//*[@id="s-lc-content-eqlist-67826"]/div/ul[4]/li/a',
        "Gardner Main Stacks Study Rooms": '//*[@id="s-lc-content-eqlist-67826"]/div/ul[5]/li/a',
        "Moffit All Categories": '//*[@id="s-lc-content-eqlist-67826"]/div/ul[6]/li[1]/a'
    }

    # Check if the provided library name exists in the mapping
    if library_name in library_xpath_mapping:
        # Get the corresponding XPath expression for the selected library
        library_xpath = library_xpath_mapping[library_name]
        
        # Locate and click on the library selection element
        library_select = driver.find_element(By.XPATH, library_xpath)
        library_select.click()
    else:
        print(f"Library '{library_name}' not found in the mapping.")


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

# Prompt the user to choose a library
print("Choose a library:")
print("1. Earth Sciences & Map Seminar Room")
print("2. East Asian Library Study Rooms")
print("3. Environmental Design Library Group Study Room")
print("4. IGS Library (Matsui Center) Study Room")
print("5. Gardner Main Stacks Study Rooms")
print("6. All Categories")

# Get the user's choice
user_choice = input("Enter the number of your choice: ")

# Map user's choice to the corresponding library name
library_choices = {
    "1": "Earth Sciences & Map Seminar Room",
    "2": "East Asian Library Study Rooms",
    "3": "Environmental Design Library Group Study Room",
    "4": "IGS Library (Matsui Center) Study Room",
    "5": "Gardner Main Stacks Study Rooms",
    "6": "Moffit All Categories"
}

if user_choice in library_choices:
    selected_library = library_choices[user_choice]
    select_library(selected_library)  # Call the select_library function with the chosen library
else:
    print("Invalid choice. Please enter a valid number.")

select_date(date)
select_time_slots(start_times)
submit_booking()
