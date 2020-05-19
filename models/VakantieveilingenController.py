from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import json
import time
import datetime


class VakantieveilingenController:
    def __init__(self):
        self.browser = webdriver.Firefox()

    def login(self, username):
        print("Fetching password")
        password = VakantieveilingenController.check_credentials(username)
        if password is not None:
            print("Found password, continueing to login page")

            self.browser.get('https://www.vakantieveilingen.be/login.html')
            time.sleep(2)

            username_input = self.browser.find_element_by_name("login")
            username_input.send_keys(username)

            password_input = self.browser.find_element_by_name("password")
            password_input.send_keys(password)
            password_input.send_keys(Keys.ENTER)

            print("Entered credentials")
            time.sleep(8)

            return True

        else:
            return False

    def explore_products(self, amount):
        self.browser.get('https://www.vakantieveilingen.be/producten.html?amount=%s' % amount)
        time.sleep(2)

        auctions = []
        auction_blocks = self.browser.find_elements_by_class_name('auction-block')
        for auction_block in auction_blocks:
            link = auction_block.find_element_by_tag_name('a').get_attribute('href')
            deadline = VakantieveilingenController.get_deadline(auction_block)

            auctions.append({
                'url': link,
                'deadline': deadline
            })

        return auctions

    def process_auction(self, auction):
        self.browser.get(auction['url'])
        time.sleep(2)

        return {
            'extra_costs': self.get_extra_cost(),
            'retail_price': self.get_retail_price(),
            'supplier_link': self.get_supplier_link(),
            'category': self.get_category(),
        }

    def get_extra_cost(self):
        try:
            cost_elements = self.browser.find_elements_by_class_name('extra-costs__cost')
            return sum([
                VakantieveilingenController.price_to_float(cost_element.text)
                for cost_element in cost_elements
            ])

        except Exception:
            return None

    def get_retail_price(self):
        try:
            return VakantieveilingenController.price_to_float(
                self.browser.find_element_by_class_name('retail-price').text
            )
        except Exception:
            return None

    def get_supplier_link(self):
        try:
            return self.browser.find_element_by_css_selector('a.auction-supplier-link').get_attribute('href')

        except Exception:
            return None

    def get_category(self):
        try:
            return self.browser.find_element_by_id('breadcrumb').find_elements_by_tag_name('a')[-1].text

        except Exception:
            return None

    @staticmethod
    def check_credentials(username):
        with open('./data/credentials.json', 'r') as f:
            data = json.load(f)

        return data.get(username, None)

    @staticmethod
    def get_deadline(auction_block):
        try:
            list_of_time = auction_block.find_element_by_class_name('display-time-value').text.split(':')
            current_time = datetime.datetime.now()

            return current_time + datetime.timedelta(
                hours=int(list_of_time[0]), minutes=int(list_of_time[1]), seconds=int(list_of_time[2])
            )

        except Exception:
            return None

    @staticmethod
    def price_to_float(price_text):
        try:
            # make sure there's always .00 at the end for regex to match
            return float(re.search('\d+,\d+', '%s,00' % price_text).group(0).replace(',', '.'))

        except Exception:
            return None
