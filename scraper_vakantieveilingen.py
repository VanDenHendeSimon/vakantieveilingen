import requests
from bs4 import BeautifulSoup
import time
import datetime
import json
import re
import subprocess

# Set global variables
json_path = './data/vakantieveilingen.json'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'
}

while True:
    print('-' * 60)
    try:
        with open(json_path) as in_file:
            data = json.load(in_file)
    except Exception:
        # No json file present
        data = {}

    if len(data) > 0:
        print('Currently checking: ')
        try:
            for key in data.keys():
                # Convert deadline from string to datetime object
                deadline = datetime.datetime.strptime(
                    str(data[key]['deadline']), '%Y-%m-%dT%H:%M:%S'
                )
                # Fetch current time as datetime object
                now = datetime.datetime.now()
                # Get the amount of seconds until the deadline
                time_diff = (deadline - now).total_seconds()

                # The keys of the dictionaries are the urls that have been stored
                page = requests.get(key, headers=headers)
                soup = BeautifulSoup(page.content, 'html.parser')

                # Fetch the highest bid at this time
                highest_bid = float(soup.find(id='jsMainLotCurrentBid').get_text())
                # Compare this amount vs the amount you are willing to give,
                # including any additional fees
                price_diff = int(data[key]['max_bid']) - int(highest_bid)

                # Check whether it is worth continuing
                if time_diff > 0 and price_diff > 0:
                    # Make the time diff readable for print statement
                    s = time_diff
                    hours = s // 3600
                    s = s - (hours * 3600)
                    minutes = s // 60
                    seconds = s - (minutes * 60)
                    # total time
                    time_diff_readable = '{:02}h:{:02}m:{:02}s'.format(
                        int(hours), int(minutes), int(seconds)
                    )
                    print('%s, %s remaining, currently at €%d, willing to bid €%d' % (
                        data[key]['title'],
                        time_diff_readable,
                        int(highest_bid),
                        int(data[key]['max_bid']))
                        )

                    # When we get close to the deadline, proceed bidding process
                    if time_diff < 100:
                        # Create python script for this url and price
                        python_path = './scripts/%s.py' % re.sub('[\\W_]+', '_', key)
                        python_code = """
import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import os

headers = dict([('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0')])

# Connect to browser
browser = webdriver.Firefox()
browser.get('{url}')

proceed_to_login_btn = browser.find_element_by_xpath("//*[@id='loginToBidButton']")
proceed_to_login_btn.click()

user_name = browser.find_element_by_xpath("/html/body/div[3]/article/div/div/div[3]/div/div/form/div[1]/input")
user_name.send_keys('mysupersecretemailadress')
ww = browser.find_element_by_xpath("/html/body/div[3]/article/div/div/div[3]/div/div/form/div[2]/input")
ww.send_keys('mysupersecretpassword')
login = browser.find_element_by_xpath("//*[@id='login_submit']")
login.click()

bidding_box = browser.find_element_by_xpath("//*[@id='jsActiveBidInput']")

deadline = datetime.datetime.strptime('{deadline}', '%Y-%m-%dT%H:%M:%S')

while(True):
    now = datetime.datetime.now()

    time_diff = (deadline - now).total_seconds()

    # Close to deadline
    if time_diff <= 5:
        page = requests.get('{url}', headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        price = int(soup.find(id='jsMainLotCurrentBid').get_text())

        print('pulled price: %d' % price)

        price_diff = {max_price} - price - 1
        if price_diff >= 0:
            if time_diff <= 3:
                bid = str(price + 1)

                bidding_box.clear()
                bidding_box.send_keys(bid)
                bidding_box.send_keys(Keys.RETURN)

                print('Bid %s!' % bid)
                os.remove('{file_path}')
                print('file removed')
                exit()
        else:
            print('Too expensive')
            os.remove('{file_path}')
            exit()

    print('willing to bid %d, %ds remaining' % ({max_price}, time_diff))
    time.sleep(1/3)

""".format(
                            url=key,
                            deadline=str(data[key]['deadline']),
                            max_price=int(data[key]['max_bid']),
                            file_path=python_path
                        )

                        with open(python_path, 'w') as py_file:
                            py_file.write(python_code)

                        # Launch python file
                        cmd = 'python %s' % python_path
                        subprocess.Popen(cmd, shell=False)

                        # Update json, so we don't bid on the same item at the same time
                        del data[key]
                        with open(json_path, 'w') as json_out:
                            json.dump(data, json_out)
                        print(
                            'Removed %s from cart bcus it made it to the next round' % key
                        )
                        break

                else:
                    # Either too expensive or too late

                    # Remove the item from the basket
                    del data[key]

                    # Update json
                    with open(json_path, 'w') as json_out:
                        json.dump(data, json_out)

                    # User feedback
                    if time_diff < 0:
                        print(
                            'Removed %s from cart bcus of time diff %d' % (
                                key, time_diff
                            )
                        )
                    else:
                        print(
                            'Removed %s from cart bcus of price diff %d' % (
                                key, price_diff
                            )
                        )
        except RuntimeError:
            print('RuntimeError')

    # Check every 60 seconds
    time.sleep(60)
