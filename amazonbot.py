from datetime import datetime

import bs4
import sys
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from twilio.rest import Client
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from twilio.base.exceptions import TwilioRestException
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

import notify
# Amazon credentials
username = 'tuh39308@temple.edu'
password = 'Bd02241997'
csv = '846'


def time_sleep(x, driver):
    for i in range(x, -1, -1):
        sys.stdout.write('\r')
        sys.stdout.write('{:2d} seconds'.format(i))
        sys.stdout.flush()
        time.sleep(1)
    driver.execute_script('window.localStorage.clear();')
    driver.refresh()
    sys.stdout.write('\r')
    sys.stdout.write('Page refreshed\n')
    sys.stdout.flush()


def create_driver():
    """Creating driver."""
    options = Options()
    options.headless = False  # Change To False if you want to see Firefox Browser Again.
    profile = webdriver.FirefoxProfile(r'C:\Users\igamb\AppData\Roaming\Mozilla\Firefox\Profiles\ecdn3awe.default-release')
    driver = webdriver.Firefox(profile, options=options, executable_path=GeckoDriverManager().install())
    return driver


def driver_wait(driver, find_type, selector):
    """Driver Wait Settings."""
    while True:
        if find_type == 'css':
            try:
                driver.find_element_by_css_selector(selector).click()
                break
            except NoSuchElementException:
                driver.implicitly_wait(0.2)
        elif find_type == 'name':
            try:
                driver.find_element_by_name(selector).click()
                break
            except NoSuchElementException:
                driver.implicitly_wait(0.2)


def login_attempt(driver):
    """Attempting to login Amazon Account."""
    driver.get('https://www.amazon.com/gp/sign-in.html')
    try:
        username_field = driver.find_element_by_css_selector('#ap_email')
        username_field.send_keys(username)
        driver_wait(driver, 'css', '#continue')
        password_field = driver.find_element_by_css_selector('#ap_password')
        password_field.send_keys(password)
        driver_wait(driver, 'css', '#signInSubmit')
        time.sleep(2)
    except NoSuchElementException:
        pass
    driver.get('https://www.amazon.com/dp/B08L8L71SM?smid=ATVPDKIKX0DER&tag=fixitservices-20')


def finding_cards(driver):
    """Scanning all cards."""
    while True:
        time.sleep(1)
        html = driver.page_source
        soup = bs4.BeautifulSoup(html, 'html.parser')
        try:
            find_all_cards = soup.find_all('span', {'class': 'style__text__2xIA2'})
            for card in find_all_cards:
                if 'Add to Cart' in card.get_text():
                    print('Card Available!')
                    driver_wait(driver, 'css', '.style__addToCart__9TqqV')
                    driver.get('https://www.amazon.com/gp/cart/view.html?ref_=nav_cart')
                    driver_wait(driver, 'css', '.a-button-input')
                    try:
                        asking_to_login = driver.find_element_by_css_selector('#ap_password').is_displayed()
                        if asking_to_login:
                            driver.find_element_by_css_selector('#ap_password').send_keys(password)
                            driver_wait(driver, 'css', '#signInSubmit')
                    except NoSuchElementException:
                        pass
                    driver_wait(driver, 'css', '.a-button-input')  # Final Checkout Button!
                    print('Order Placed')

                    for i in range(3):
                        print('\a')
                        time.sleep(1)
                    time.sleep(1800)
                    driver.quit()
                    return
        except (AttributeError, NoSuchElementException, TimeoutError):
            pass
        time_sleep(5, driver)

def checkCart(driver):
    isComplete = False
    while not isComplete:
        # find add to cart button
        try:
            atcBtn = WebDriverWait(driver, 1.5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.a-fixed-right-grid:nth-child(3) > div:nth-child(1) > div:nth-child(2) > form:nth-child(1) > span:nth-child(12) > span:nth-child(1) > span:nth-child(1) > input:nth-child(1)"))
            )
        except:
            print('Add to cart button not found')
            print('Refreshing')
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print("Current Time =", current_time)
            print('...................................')
            print('\n')
            driver.refresh()
            continue

        print("Add to cart button found")
        atcBtn.click()
        driver.get('https://www.amazon.com/gp/cart/view.html?ref_=nav_cart')
        driver_wait(driver, 'css', '.a-button-input')
        driver_wait(driver, 'name', 'submissionURL')
        driver_wait(driver, 'css', '#orderSummaryPrimaryActionBtn > span:nth-child(1) > input:nth-child(1)')
        driver_wait(driver, 'name', 'ppw-instrumentRowSelection')
        driver_wait(driver, 'css', '#orderSummaryPrimaryActionBtn > span:nth-child(1) > input:nth-child(1)')  # Final Checkout Button!
        time.sleep(2)
        driver_wait(driver, 'css', 'div.shipping-speed:nth-child(2) > div:nth-child(2) > label:nth-child(1) > input:nth-child(1)')
        driver_wait(driver, 'css', '#submitOrderButtonId > span:nth-child(1) > input:nth-child(1)')
        print('Order Placed')
    isComplete = True

if __name__ == '__main__':
    driver = create_driver()
    login_attempt(driver)
    #finding_cards(driver)
    checkCart(driver)