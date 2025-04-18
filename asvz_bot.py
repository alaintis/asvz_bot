from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
import time
import random
from selenium.webdriver.common.action_chains import ActionChains


# ---- CONFIG ----
ETHZ_USERNAME = "username"
ETHZ_PASSWORD = "password"


#Hardcoded for testin
LESSON_URL = "https://schalter.asvz.ch/tn/lessons/676708"

#For actual use 
#LESSON_URL = input("Enter the full ASVZ lesson URL: ").strip()

# Set up browser
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # optional: run without opening a window
driver = webdriver.Chrome(options=options)

# STEP 1: Go to ASVZ login
driver.get("https://auth.asvz.ch/Account/Login?ReturnUrl=%2FManage%2FIndex")

# STEP 2: Click "Login SwitchAai"
wait = WebDriverWait(driver, 10)
login_button = wait.until(EC.element_to_be_clickable((By.NAME, "provider")))
login_button.click()

## Step 3: Click the dropdown icon to reveal list of institutions
wait.until(EC.element_to_be_clickable((By.ID, "userIdPSelection_iddicon"))).click()

# Step 4: Wait and click on ETH Zurich in the dropdown
eth_option_xpath = '//div[@savedvalue="https://aai-logon.ethz.ch/idp/shibboleth" and contains(text(), "ETH Zurich")]'
wait.until(EC.visibility_of_element_located((By.XPATH, eth_option_xpath))).click()

# Step 5: Click the "Weiter" or continue button
#wait.until(EC.element_to_be_clickable((By.NAME, "Select"))).click()

# Step 6: ETH Login Page (wait for username field to appear)
# Wait until username input is visible AND interactable
# You've just clicked on ETH Zurich in the dropdown and landed on the ETH login page

# Confirm page has loaded
wait.until(EC.presence_of_element_located((By.ID, "username")))

# Take a screenshot to debug the form visibility
driver.save_screenshot("eth_login_visible.png")  # 👈 put it here

# Pause briefly to make sure everything renders
time.sleep(2)

# Now try to input using JS
driver.execute_script("document.getElementsByName('j_username')[0].value = arguments[0];", ETHZ_USERNAME)
driver.execute_script("document.getElementsByName('j_password')[0].value = arguments[0];", ETHZ_PASSWORD)

# Optional: check it worked
username_check = driver.execute_script("return document.getElementsByName('j_username')[0].value;")
print(f"✅ Username filled: {username_check}")


time.sleep(2)

# Click login button
driver.execute_script("document.getElementsByName('_eventId_proceed')[0].click();")
time.sleep(8)

try:
    schalter_link = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Online-Schalter"))
    )
    print("🟢 Found 'Online-Schalter' link. Clicking it...")
    schalter_link.click()
    time.sleep(2)  # Let the redirect happen
except:
    print("🔍 'Online-Schalter' not present — skipping.")

driver.get(LESSON_URL)

def simulate_human_activity(driver):
    # Random scroll (up or down a bit)
    scroll_distance = random.randint(-100, 100)
    driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
    print(f"🌀 Scrolled by {scroll_distance}px")

    # Random delay between scroll and click
    time.sleep(random.uniform(0.3, 1.5))

    # Try to move and click somewhere around the "Niveau" field
    try:
        niveau_element = driver.find_element(By.XPATH, '//dt[contains(text(), "Niveau")]')
        action = ActionChains(driver)

        # Move to random offset within the element
        offset_x = random.randint(0, 30)
        offset_y = random.randint(0, 10)
        action.move_to_element_with_offset(niveau_element, offset_x, offset_y).click().perform()
        print(f"👆 Clicked near 'Niveau' at offset ({offset_x}, {offset_y})")
    except Exception as e:
        print(f"⚠️ Could not interact with Niveau element: {e}")


last_interaction = time.time()
next_interaction_interval = random.randint(30, 70)  # initial delay

while True:
    try:
        button = driver.find_element(By.ID, "btnRegister")
        if button.is_displayed() and button.is_enabled():
            print("✅ Button is active! Clicking now...")
            driver.execute_script("arguments[0].click();", button)
            break
    except:
        pass

    # Every X seconds, simulate random activity
    if time.time() - last_interaction > next_interaction_interval:
        simulate_human_activity(driver)
        last_interaction = time.time()
        next_interaction_interval = random.randint(30, 70)  # set new random interval

    time.sleep(0.2)





# Keep the browser open or close:
# driver.quit()
