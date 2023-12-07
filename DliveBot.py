#!/usr/bin/env python3
"""
    *******************************************************************************************
    DliveBot.
    Author: Ali Toori, Python Developer [Web-Automation Bot Developer | Web-Scraper Developer]
    Profiles:
        Upwork: https://www.upwork.com/freelancers/~011f08f1c849755c46
        Fiver: https://www.fiverr.com/alitoori
    *******************************************************************************************
"""
import os
import time
import ntplib
import random
import pyfiglet
import datetime
import pandas as pd
import logging.config
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC

logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    'formatters': {
        'colored': {
            '()': 'colorlog.ColoredFormatter',  # colored output
            # --> %(log_color)s is very important, that's what colors the line
            'format': '[%(asctime)s] %(log_color)s%(message)s'
        },
    },
    "handlers": {
        "console": {
            "class": "colorlog.StreamHandler",
            "level": "INFO",
            "formatter": "colored",
            "stream": "ext://sys.stdout"
        }
    },
    "root": {
        "level": "INFO",
        "handlers": [
            "console"
        ]
    }
})

LOGGER = logging.getLogger()

DLIVE_HOME_URL = "https://dlive.tv/"
DLIVE_URL_CHATTING = "https://dlive.tv/s/browse/9967/Chatting"


class Dlive:

    def __init__(self):
        self.first_time = True
        self.PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

    # Get random user-agent
    def get_random_user_agent(self):
        file_path = os.path.join(self.PROJECT_ROOT, 'DliveRes/user_agents.txt')
        user_agents_list = []
        with open(file_path) as f:
            content = f.readlines()
        user_agents_list = [x.strip() for x in content]
        return random.choice(user_agents_list)

    # Get web driver
    def get_driver(self):
        # For absolute chromedriver path
        PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
        DRIVER_BIN = os.path.join(PROJECT_ROOT, "bin/chromedriver_win32.exe")
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-blink-features")
        # options.add_argument("--user-data-dir=chrome-data")
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument(F'--user-agent={self.get_random_user_agent()}')
        # options.add_argument('--headless')
        # driver = webdriver.Chrome(executable_path=DRIVER_BIN, options=options)
        driver = webdriver.Chrome(executable_path=DRIVER_BIN, options=options)
        return driver

    # Login to the website
    def login_dlive(self, driver):
        # dir_path_session = os.path.join(self.PROJECT_ROOT, 'chrome-data')
        # if os.path.isdir(dir_path_session):
        #     return True
        headers = {
            'authority': 'graphigo.prd.dlive.tv',
            'fingerprint': '50d5df36d47af5ec1487e889865c19bf',
            'gacid': '2077235078.1601370353',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
            'x-dlive-mversion': 'v0.6.09',
            'accept': '*/*',
            'x-dlive-mtype': 'web',
            'content-type': 'application/json',
            'x-dlive-mid': '50d5df36d47af5ec1487e889865c19bf',
            'origin': 'https://dlive.tv',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://dlive.tv/s/browse/9967/Chatting',
            'accept-language': 'en-US,en;q=0.9',
        }

        data = {
            'operationName': 'EmailLogin',
            'variables': {'email': 'CherryKick@onme.info', 'password': 'password1!'},
            'extensions': {'persistedQuery': {'version': '1',
                                              'sha256Hash': 'ee5f1abab8122a4441ed378b01f0905612ce3e053c80c1eb1f15cd28310ff017'
                                              }
                           }
        }
        # response = requests.post('https://graphigo.prd.dlive.tv/', headers=headers, data=data)
        # If cookies login filed, try logging-in normally
        file_path_account = os.path.join(self.PROJECT_ROOT, 'DliveRes/Account.txt')
        # Get account from input file
        with open(file_path_account) as f:
            content = f.readlines()
        account = [x.strip() for x in content[0].split(':')]
        LOGGER.info(f"[Account ID: {str(account)}]")
        LOGGER.info(f"[Requesting page: {str(DLIVE_URL_CHATTING)}]")
        driver.get(DLIVE_URL_CHATTING)
        # Try logging-in
        try:
            try:
                LOGGER.info("[Waiting for login button to become visible")
                wait_until_visible(driver=driver, class_name='text-xs-right', duration=20)
                driver.find_element_by_class_name('text-xs-right').find_elements_by_tag_name('div')[3].click()
            except:
                try:
                    LOGGER.info("[Waiting for login button to become visible")
                    wait_until_visible(driver=driver, class_name='text-xs-right', duration=10)
                    driver.find_element_by_class_name('text-xs-right').find_elements_by_tag_name('div')[4].click()
                except:
                    pass
            LOGGER.info("[Waiting for login fields to become visible]")
            wait_until_visible(driver=driver, class_name='v-text-field__slot', duration=20)
            # Filling login fields
            try:
                LOGGER.info(f"[Filling username: {str(account[0])}]")
                email_input = driver.find_element_by_tag_name('form').find_elements_by_tag_name('input')[0]
                email_input.send_keys(account[0])
                LOGGER.info(f"[Filling password: {str(account[1])}]")
                password_input = driver.find_element_by_tag_name('form').find_elements_by_tag_name('input')[1]
                password_input.send_keys(account[1])
                LOGGER.info(f"[Signing in as: {account[0]}]")
            except WebDriverException as ec:
                LOGGER.warning("Couldn't filled the login fields")
                LOGGER.info(ec.msg)
                LOGGER.info(f"[Filling username: {str(account[0])}]")
                email_input = driver.find_elements_by_class_name('v-text-field__slot').find_element_by_tag_name('input')
                email_input.send_keys(account[0])
                LOGGER.info(f"[Filling password: {str(account[1])}]")
                password_input = driver.find_elements_by_class_name('v-text-field__slot')[1].find_element_by_tag_name('input')
                password_input.send_keys(account[1])
                LOGGER.info(f"[Signing in as: {account[0]}]")
            # Clicking button login
            try:
                driver.find_element_by_tag_name('form').find_elements_by_tag_name('div')[10].click()
            except:
                LOGGER.warning("Couldn't click button login")
                try:
                    driver.find_element_by_tag_name('form').find_elements_by_tag_name('div')[11].click()
                except:
                    LOGGER.critical("Couldn't click button login")
                    try:
                        driver.find_element_by_xpath('//*[@id="genius"]/div[9]/div/div/div[1]/div[2]/div/div/div[1]/div/div[1]/div[1]/form/div[3]').click()
                    except:
                        LOGGER.error("Couldn't click button login")
                        pass
            LOGGER.info("[Waiting for profile to become visible]")
            wait_until_visible(driver=driver, xpath='//*[@id="router-view"]/div/div[2]/div/div[1]/div[1]/div[2]/h1')
            LOGGER.info(f"[Successfully logged in as {account[0]}]")
        except WebDriverException as ec:
            LOGGER.error("[Exception during login-in]: " + str(ec.msg))
            pass

    # Follow top accounts' followers
    def follow(self):
        driver = self.get_driver()
        LOGGER.info('[DliveBot launched]')
        LOGGER.info('[Signing-in to the Dlive]')
        # Sign-in to the website
        logged_in = self.login_dlive(driver)
        if logged_in:
            LOGGER.info("[Already logged-in]")
        file_path_comments = os.path.join(self.PROJECT_ROOT, 'DliveRes/Comments.txt')
        file_dlive_temp = os.path.join(self.PROJECT_ROOT, 'DliveRes/DliveTemp.csv')
        # Get Comments from input file
        with open(file_path_comments) as f:
            content = f.readlines()
        comments = [x.strip() for x in content]
        LOGGER.info(f"[Comments: {str(comments)}]")
        # df_dlive_temp = pd.read_csv(file_dlive_temp, index_col=None)
        try:
            LOGGER.info(f"Requesting page: {str(DLIVE_URL_CHATTING)}]")
            driver.get(DLIVE_URL_CHATTING)
            LOGGER.info("[Waiting for the page to become visible]")
            wait_until_visible(driver, xpath='//*[@id="router-view"]/div/div[2]/div/div[1]/div[1]/div[2]/h1')
            language_selector = driver.find_element_by_class_name('v-select__slot')
            language_selector.click()
            try:
                LOGGER.info("[Selecting language as English]")
                language_selector.find_element_by_tag_name('input').send_keys('English')
                LOGGER.info("[Language selected as English]")
            except:
                LOGGER.warning("[Language couldn't be set]")
                pass
            sleep(5)
            # driver.find_element_by_xpath('//*[@id="genius"]/div[1]/div/div/div[2]/a/div').click()
        except WebDriverException as ec:
            LOGGER.exception("[Exception while selecting language]: " + str(ec.msg))
            pass
        # try scrolling down:
        LOGGER.info("[Scrolling down the page]")
        scroll_count = 0
        while True:
            driver.find_element_by_tag_name('html').send_keys(Keys.END)
            scroll_count += 1
            if scroll_count >= 12:
                break
            try:
                wait_until_visible(driver, xpath='//*[@id="router-view"]/div/div[2]/div/div[3]/div/div/div[3]', duration=1)
                end = str(driver.find_element_by_xpath('//*[@id="router-view"]/div/div[2]/div/div[3]/div/div/div[3]').text).strip()
                if 'No more data' in end:
                    break
            except:
                pass
        # Grab account links
        LOGGER.info("[Grabbing streams]")
        streams = [stream.find_element_by_tag_name('a').get_attribute('href') for stream in driver.find_elements_by_class_name('livestream-wrapper')]
        LOGGER.info(f"[Streams found: {str(len(streams))}]")
        for stream in streams:
            LOGGER.info(f"Requesting page: {str(stream)}]")
            driver.get(stream)
            # Wait for the stream to become visible
            try:
                LOGGER.info("[Waiting for the stream to become visible]")
                wait_until_visible(driver, xpath='//*[@id="router-view"]/div/div/div[1]/div/div[1]/div[1]/div[1]/div[1]/div/img', duration=20)
                driver.find_element_by_xpath('//*[@id="router-view"]/div/div/div[1]/div/div[1]/div[1]/div[1]/div[1]/div/img').click()
                driver.find_element_by_tag_name('html').send_keys(Keys.SPACE)
            except:
                driver.refresh()
                LOGGER.info("[Waiting for the stream to become visible]")
                wait_until_visible(driver, xpath='//*[@id="router-view"]/div/div/div[1]/div/div[1]/div[1]/div[1]/div[1]/div/img')
                driver.find_element_by_xpath('//*[@id="router-view"]/div/div/div[1]/div/div[1]/div[1]/div[1]/div[1]/div/img').click()
                driver.find_element_by_tag_name('html').send_keys(Keys.SPACE)
                pass
            # Try clicking the button followers
            try:
                LOGGER.info("[Waiting for the followers button to become clickable]")
                wait_until_clickable(driver, xpath='//*[@id="router-view"]/div/div/div[1]/div/div[2]/div/div/div[1]/a[6]/span[1]', duration=20)
                LOGGER.info("[Clicking the followers button]")
                driver.find_element_by_xpath('//*[@id="router-view"]/div/div/div[1]/div/div[2]/div/div/div[1]/a[6]/span[1]').click()
            except:
                driver.refresh()
                LOGGER.info("[Waiting for the followers button to become clickable]")
                wait_until_clickable(driver, xpath='//*[@id="router-view"]/div/div/div[1]/div/div[2]/div/div/div[1]/a[6]')
                LOGGER.info("[Clicking the followers button]")
                driver.find_element_by_xpath('//*[@id="router-view"]/div/div/div[1]/div/div[2]/div/div/div[1]/a[6]').click()
            # Try to view the followers
            try:
                LOGGER.info("[Waiting for the followers to become visible]")
                wait_until_visible(driver, css_selector='.flex-align-center.clickable', duration=20)
            except:
                pass
            # Try to check the number of followers and skip the stream if less than 200
            try:
                LOGGER.info("[Waiting for the followers counter to become visible]")
                wait_until_visible(driver, xpath='//*[@id="router-view"]/div/div/div[1]/div/div[2]/div/div/div[1]/a[6]/span[2]/span[2]', duration=20)
                followers_count = str(driver.find_element_by_xpath('//*[@id="router-view"]/div/div/div[1]/div/div[2]/div/div/div[1]/a[6]/span[2]/span[2]').text).strip()
                LOGGER.info(f"[Followers count {followers_count}]")
                if int(followers_count) < 200:
                    continue
            except:
                pass
            # try scrolling down the followers:
            LOGGER.info("[Scrolling down the followers]")
            scroll_count = 0
            while True:
                driver.find_element_by_tag_name('html').send_keys(Keys.END)
                scroll_count += 1
                if scroll_count >= 12:
                    break
                try:
                    wait_until_visible(driver, xpath='//*[@id="router-view"]/div/div[2]/div/div[3]/div/div/div[3]', duration=3)
                    end = str(driver.find_element_by_xpath('//*[@id="router-view"]/div/div[2]/div/div[3]/div/div/div[3]').text).strip()
                    if 'No more data' in end:
                        break
                except:
                    pass
            # Grab account links
            sleep(3)
            LOGGER.info("[Grabbing followers]")
            followers = [follower.get_attribute('href') for follower in driver.find_elements_by_css_selector('.flex-align-center.clickable')]
            LOGGER.info(f"[Followers found: {str(len(followers))}]")
            # followers = [follower.get_attribute('href') for follower in driver.find_element_by_class_name('v-window__container').find_elements_by_tag_name('a')]
            # LOGGER.info(f"[Followers found: {str(len(followers))}]")
            LOGGER.info(f"[Followers: {str(followers)}]")
            LOGGER.info("[Starting to follow top 200 followers]")
            # Follow and send text the followers
            for follower in followers[:200]:
                LOGGER.info(f"Requesting page: {str(follower)}]")
                driver.get(follower)
                LOGGER.info(f"[Follower number: {str(followers.index(follower) + 1)}]")
                LOGGER.info(f"[Following: {str(follower[17:])}]")
                comment = random.choice(comments)
                # Check and skip if channel has been suspended or deactivated
                try:
                    wait_until_visible(driver, xpath='//*[@id="channel-suspended"]', duration=20)
                    suspended_text = str(driver.find_element_by_xpath('//*[@id="channel-suspended"]').text).strip()
                    if 'channel has been' in suspended_text:
                        LOGGER.warning(f"[Channel Suspended or Deactivated]: {suspended_text}")
                        continue
                except:
                    pass
                LOGGER.info("[Waiting for the follower's page to become visible]")
                wait_until_visible(driver, xpath='//*[@id="router-view"]/div/div/div[1]/div/div[1]/div[1]/div[1]/div[1]/div/img')
                # Try clicking follow button to follow the streamer
                try:
                    LOGGER.info("[Waiting for the follow button to become visible]")
                    wait_until_visible(driver, xpath='//*[@id="router-view"]/div/div/div[1]/div/div[1]/div[1]/div[2]/div[2]/div/div[1]/div', duration=30)
                    btn_follow = driver.find_element_by_xpath('//*[@id="router-view"]/div/div/div[1]/div/div[1]/div[1]/div[2]/div[2]/div/div[1]/div')
                    if 'Followed' in str(btn_follow.text).strip():
                        continue
                    btn_follow.click()
                    LOGGER.info(f"[Followed: {str(follower[17:])}]")
                except:
                    driver.refresh()
                    LOGGER.info("[Waiting for the follow button to become visible]")
                    wait_until_visible(driver, xpath='//*[@id="router-view"]/div/div/div[1]/div/div[1]/div[1]/div[2]/div[2]/div/div[1]/div/div')
                    driver.find_element_by_xpath('//*[@id="router-view"]/div/div/div[1]/div/div[1]/div[1]/div[2]/div[2]/div/div[1]/div/div').click()
                    LOGGER.info(f"[Followed: {str(follower[17:])}]")
                    pass
                # Try sending text message to the streamer
                try:
                    LOGGER.info("[Waiting for the message box to become visible]")
                    wait_until_visible(driver, xpath='//*[@id="chatroom"]/div[3]/div[2]/div[1]/div[1]/div/div/div/div/textarea')
                    text_box = driver.find_element_by_xpath('//*[@id="chatroom"]/div[3]/div[2]/div[1]/div[1]/div/div/div/div/textarea')
                    LOGGER.info(f"[Text to be sent: {str(comment)}]")
                    LOGGER.info(f"[Sending text to: {str(follower[17:])}]")
                    text_box.send_keys(comment)
                    text_box.send_keys(Keys.ENTER)
                    LOGGER.info(f"[Text has been sent to: {str(follower[17:])}]")
                except:
                    pass
                LOGGER.info("Waiting for 12 seconds")
                sleep(12)
        # Try quit the browser
        self.finish(driver)

    def finish(self, driver):
        try:
            driver.close()
            driver.quit()
        except WebDriverException as exc:
            print('Problem occurred while closing the WebDriver instance ...', exc.args)


def wait_until_clickable(driver, xpath=None, element_id=None, name=None, class_name=None, css_selector=None,
                         duration=10000, frequency=0.01):
    if xpath:
        WebDriverWait(driver, duration, frequency).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    elif element_id:
        WebDriverWait(driver, duration, frequency).until(EC.element_to_be_clickable((By.ID, element_id)))
    elif name:
        WebDriverWait(driver, duration, frequency).until(EC.element_to_be_clickable((By.NAME, name)))
    elif class_name:
        WebDriverWait(driver, duration, frequency).until(EC.element_to_be_clickable((By.CLASS_NAME, class_name)))
    elif css_selector:
        WebDriverWait(driver, duration, frequency).until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))


def wait_until_visible(driver, xpath=None, element_id=None, name=None, class_name=None, css_selector=None,
                       duration=10000, frequency=0.01):
    if xpath:
        WebDriverWait(driver, duration, frequency).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    elif element_id:
        WebDriverWait(driver, duration, frequency).until(EC.visibility_of_element_located((By.ID, element_id)))
    elif name:
        WebDriverWait(driver, duration, frequency).until(EC.visibility_of_element_located((By.NAME, name)))
    elif class_name:
        WebDriverWait(driver, duration, frequency).until(EC.visibility_of_element_located((By.CLASS_NAME, class_name)))
    elif css_selector:
        WebDriverWait(driver, duration, frequency).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector)))


def main():
    dlive = Dlive()
    # Getting Day before Yesterday
    # day_before_yesterday = (datetime.datetime.now() - datetime.timedelta(2)).strftime('%m/%d/%Y')
    while True:
        dlive.follow()
    # except WebDriverException as exc:
    #     print('Exception in WebDriver:', exc.msg)


# Trial version logic
def trial(trial_date):
    ntp_client = ntplib.NTPClient()
    response = ntp_client.request('pool.ntp.org')
    local_time = time.localtime(response.ref_time)
    current_date = time.strftime('%Y-%m-%d %H:%M:%S', local_time)
    current_date = datetime.datetime.strptime(current_date, '%Y-%m-%d %H:%M:%S')
    return trial_date > current_date


if __name__ == '__main__':
    trial_date = datetime.datetime.strptime('2020-11-17 23:59:59', '%Y-%m-%d %H:%M:%S')
    # Print ASCII Art
    print('************************************************************************\n')
    pyfiglet.print_figlet('____________                DliveBot ____________\n', colors='RED')
    print('Author: Ali Toori, Python Developer [Web-Automation Bot Developer]\n'
          'Profiles:\n\tUpwork: https://www.upwork.com/freelancers/~011f08f1c849755c46\n\t'
          'Fiver: https://www.fiverr.com/alitoori\n************************************************************************')
    # Trial version logic
    if trial(trial_date):
        # print("Your trial will end on: ",
        #       str(trial_date) + ". To get full version, please contact fiverr.com/AliToori !")
        main()
    else:
        pass
        # print("Your trial has been expired, To get full version, please contact fiverr.com/AliToori !")
