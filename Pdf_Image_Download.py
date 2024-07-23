from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import os
import time
import shutil
import traceback
import sys

cd = os.getcwd()  # Get Current Directory
download_directory = cd + "\\Monthly Progress Report\\"  # Set Download Directory
if os.path.exists(download_directory):  # Check if directory exists
    shutil.rmtree(download_directory)  # Remove and Recreate directory
    os.mkdir(download_directory)
else:
    os.mkdir(download_directory)  # Create directory if it doesn't exist

# Create an instance of options
chrome_options = Options()

# Settings to download the pdf
chrome_options.add_experimental_option('prefs', {
    "download.default_directory": download_directory,  # Specify the path to download the pdf
    "download.prompt_for_download": False,  # Disable the download prompt
    "download.directory_upgrade": True,  # Upgrade the download path
    "plugins.always_open_pdf_externally": True,  # Open the pdf always externally
    "safebrowsing.enabled": True  # Enable Safe Browsing
})
chrome_options.add_argument("--safebrowsing-disable-download-protection")
chrome_options.add_argument("safebrowsing-disable-extension-blacklist")

# Initialize the chrome webdriver
driver = webdriver.Chrome(options=chrome_options)

# Maximize the Browser Window
driver.maximize_window()

# Open a website
driver.get("https://www.labour.gov.in/")

actions = ActionChains(driver)
wait = WebDriverWait(driver, 20)

try:
    # Perform the actions
    Documents = driver.find_element(By.CLASS_NAME, "menu-mlid-3952")
    actions.move_to_element(Documents).perform()  # Hover to the element
    time.sleep(2)

    MonthlyProgressReport = driver.find_element(By.CLASS_NAME, "menu-mlid-5887")
    MonthlyProgressReport.click()
    time.sleep(2)

    # Find the element using XPATH
    href_1 = "https://labour.gov.in/sites/default/files/mpr_may_2024.pdf"
    SelectReport = wait.until(EC.element_to_be_clickable((By.XPATH, f'//a[@href="{href_1}"]')))
    SelectReport.click()
    print("Downloaded Monthly Progress Report")
    time.sleep(2)

except Exception as e:
    print(f"Error: {e}")

# Wait for alert and accept it
try:
    alert = wait.until(EC.alert_is_present())
    alert.accept()
    time.sleep(2)
except Exception as e:
    print(f"Error: {e}")

# Navigate back to the previous page in the browser’s history
driver.back()
time.sleep(2)

try:
    cd = os.getcwd()
    gallery_path = cd + "\\Photo Gallery\\"
    if os.path.exists(gallery_path):
        shutil.rmtree(gallery_path)
        os.mkdir(gallery_path)
    else:
        os.mkdir(gallery_path)

    chrome_options.add_experimental_option('prefs', {
        "download.default_directory": gallery_path, 
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True,  # This will download the PDF instead of opening it
        "safebrowsing.enabled": True
    })

    # Perform the actions
    Media = wait.until(EC.visibility_of_element_located((By.XPATH, "//a[normalize-space()='Media']")))
    Media.click()
    time.sleep(2)

    More_Info = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Click for more info of Press Releases']")))
    More_Info.click()

    Photo_Gallery = wait.until(EC.element_to_be_clickable((By.XPATH, "(//a[normalize-space()='Photo Gallery'])[2]")))
    
    href_2 = Photo_Gallery.get_attribute('href')
    driver.get(href_2)

    time.sleep(5)
    window_after = driver.window_handles[0]

    Images = driver.find_elements(By.XPATH, "//table//img")
    Image_urls = [element.get_attribute('src') for element in Images[:10]]
    for i, url in enumerate(Image_urls, 1):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                with open(os.path.join(gallery_path, f"Image_{i}.jpg"), 'wb') as file:
                    file.write(response.content)
                    print(f"Downloaded Image_{i}.jpg")
            else:
                print(f"Failed to download Image_{i}.jpg")
        except Exception as e:
            print(f"Error occured while downloading Image{i}.jpg: {e}")

except Exception as e:
    print(f"Error: {e}")
    exc_type, exc_obj, tb = sys.exc_info()
    print(f"Error on line: {tb.tb_lineno}")

time.sleep(2)

# Close the WebDriver
driver.quit()