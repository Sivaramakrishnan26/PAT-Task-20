from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Initialize the chrome webdriver
driver = webdriver.Chrome()

# Maximize the browser window
driver.maximize_window()

# Open a website
driver.get("https://www.cowin.gov.in/")
time.sleep(2)

# Perform the actions
DropDownButton = driver.find_elements(By.CLASS_NAME, "dropdwnbtn")

FAQ = DropDownButton[3]
Partners = DropDownButton[4]

FAQ.click()
Partners.click()
time.sleep(2)

# Only to print Window handles
# window_handles = driver.window_handles
# print("Window Handles:")
# for handle in window_handles:
#     print(handle)

print("Window Handles:")
window_handles = driver.window_handles
# for i in range(min(3, len(window_handles))):
#     driver.switch_to.window(window_handles[i])

for handle in window_handles:
    try:
        driver.switch_to.window(handle)
        Title = driver.title
        Current_URL = driver.current_url
        print(f"{Title} : {Current_URL} : {handle}")
        time.sleep(1)
    except Exception as e:
        print(f"An Error Occured: {e}")

# Frames
frames = driver.find_elements(By.TAG_NAME, "frame")
print("Number of frames in the page:", len(frames))
for frame in frames:
    print(f"Frame ID: {frame.get_attribute('id')}")

driver.switch_to.window(driver.window_handles[1])
time.sleep(1)
driver.close()

driver.switch_to.window(driver.window_handles[1])
time.sleep(1)
driver.close()

time.sleep(1)

# Close the WebDriver
driver.quit()
