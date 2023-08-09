from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time
import random
import string
import threading

lock = threading.Lock()

def handle_cookie_banner(driver):
    try:
        cookie_banner = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='onetrust-policy']"))
        )
        close_button = cookie_banner.find_element(By.XPATH, "//*[@id='onetrust-close-btn-container']")
        close_button.click()

        # Wait for the cookie banner to disappear
        WebDriverWait(driver, 10).until_not(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='onetrust-policy']"))
        )
    except:
        pass

def create_account(email, password):
    options = webdriver.FirefoxOptions()
    options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)
    driver.get("https://www.spotify.com/in-en/signup")

    handle_cookie_banner(driver)  # Handle the cookie banner if present

    email_input = driver.find_element(By.CSS_SELECTOR, "#email")
    email_input.send_keys(email)

    password_input = driver.find_element(By.CSS_SELECTOR, "#password")
    password_input.send_keys(password)

    random_length = random.randint(6, 8)
    random_username = ''.join(random.choices(string.ascii_letters, k=random_length))
    username_input = driver.find_element(By.CSS_SELECTOR, "#displayname")
    username_input.send_keys(random_username)

    # Generate random values for year, month, and day
    random_year = str(random.randint(1990, 2000))
    random_month = random.choice(
        ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November',
         'Desember'])
    random_day = str(random.randint(1, 28))

    year_input = driver.find_element(By.CSS_SELECTOR, "#year")
    year_input.send_keys(random_year)

    # Click the month dropdown to expand it
    month_dropdown = driver.find_element(By.NAME, "month")
    month_dropdown.click()

    # Now click on the desired month option by locating it through its text value
    desired_month_option = driver.find_element(By.XPATH, f"//option[text()='{random_month}']")
    desired_month_option.click()

    day_input = driver.find_element(By.CSS_SELECTOR, "#day")
    day_input.send_keys(random_day)

    gender_label = driver.find_element(By.CSS_SELECTOR,
                                       "div.Radio-sc-tr5kfi-0:nth-child(1) > label:nth-child(2) > span:nth-child(2)")
    gender_label.click()

    finish_button = driver.find_element(By.CSS_SELECTOR, ".dqLIWu")
    finish_button.click()

    try:
        WebDriverWait(driver, 60).until(
            EC.url_contains("https://www.spotify.com/in-en/download/")
        )
    except TimeoutException:
        print(f"Encountered reCAPTCHA for email: {email}. Trying another proxy.")
        driver.quit()
        return

    with lock:  # Use lock to ensure each thread completes its registration before the next one starts
        with open("acc.txt", "a") as file:
            file.write(f"{email}:{password}\n")
            print(f"Account created - Email: {email}, Password: {password}")

    driver.quit()

threads = []
num_threads = int(input("Amount of Account: "))

password_choice = input("Password choice (1 Generated Pass, 2 Own Pass): ")

if password_choice == "1":
    password_length = random.randint(8, 12)
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=password_length))
else:
    password = input("Password: ")

for _ in range(num_threads):
    email_length = random.randint(5, 10)
    email = ''.join(random.choices(string.ascii_lowercase, k=email_length)) + "@me.tv"

    thread = threading.Thread(target=create_account, args=(email, password))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print("Accounts created successfully. Saved in acc.txt")
