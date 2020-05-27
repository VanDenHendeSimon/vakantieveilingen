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

    def buy(self, url, max_price):
        # move into a new thread / open up a new browser first? not necessary now
        auction_details = self.process_auction(url)
        auction_details.update({
            "deadline": VakantieveilingenController.get_deadline(self.browser)
        })

        time_until_deadline = auction_details['deadline'] - datetime.datetime.now()
        # Sleep until 20 seconds before the deadline
        # time.sleep(time_until_deadline.seconds - 20)
        print("Sleeping %d seconds" % (time_until_deadline.seconds - 20))

        # Get ready to buy
        now = datetime.datetime.now()
        while now < auction_details['deadline']:
            current_bid = self.get_current_bid()
            if (current_bid + auction_details['extra_costs']) < max_price:
                time_until_deadline = auction_details['deadline'] - now

                if time_until_deadline.seconds == 0:
                    # Less than a second before the deadline
                    time.sleep(max(0, (time_until_deadline.microseconds / 1000000) - 0.01))
                    self.browser.find_element_by_class_name('bid-input').send_keys(str(current_bid + 1))
                    self.browser.find_element_by_id('jsActiveBidButton').click()
                    break

                time.sleep(0.05)
                now = datetime.datetime.now()

            else:
                print("Current bid is too high.")
                print("Price: %s, max price: %s" % (
                    current_bid + auction_details['extra_costs'],
                    max_price
                ))
                break

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

    def process_auction(self, url):
        self.browser.get(url)
        time.sleep(2)

        return {
            'extra_costs': self.get_extra_cost(),
            'retail_price': self.get_retail_price(),
            'supplier_link': self.get_supplier_link(),
            'category': self.get_category(),
            'current_bid': self.get_current_bid(),
        }

    def fetch_auction_details(self, url):
        """
        This method is ran after an item has been bought
        It will collect all valuable data for a reselling post
        """
        self.browser.get(url)
        time.sleep(2)

        auction_content = self.browser.find_element_by_class_name('auction-content')

        # TODO: Test this
        title = auction_content.find_element_by_class_name('auction-title').text
        description = auction_content.find_element_by_class_name('auction-description').text
        product_details = auction_content.find_element_by_class_name('description').find_elements_by_css_selector('ul, p')

        return ''

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

    def get_current_bid(self):
        try:
            return int(self.browser.find_element_by_id('jsMainLotCurrentBid').text)

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
