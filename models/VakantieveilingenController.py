from .DataRepository import DataRepository

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

    def add_to_wishlist(self, url, max_price):
        # Inserts into database (category / auction tables)
        auction_details = self.process_auction(url)
        time.sleep(1)

        if auction_details is not None:
            DataRepository.create_wishlist(url, max_price)

    def buy(self, url, max_price):
        # move into a new thread / open up a new browser first? not necessary
        auction_details = self.process_auction(url)
        time.sleep(1)
        auction_details['deadline'] = VakantieveilingenController.get_deadline(self.browser)

        try:
            time_until_deadline = auction_details['deadline'] - datetime.datetime.now()
        except Exception:
            self.buy(url, max_price)

        print("auction details: %s" % auction_details)
        # Sleep until 20 seconds before the deadline
        print("Sleeping %d seconds" % (time_until_deadline.seconds - 20))
        time.sleep(min((time_until_deadline.seconds - 20), 0))

        # Get ready to buy
        now = datetime.datetime.now()
        while now < auction_details['deadline']:
            try:
                current_bid = self.get_current_bid()
                if (current_bid + auction_details['extra_costs']) < max_price:
                    time_until_deadline = auction_details['deadline'] - now

                    if time_until_deadline.seconds == 0:
                        # Less than a second before the deadline
                        # time.sleep(max(0, (time_until_deadline.microseconds / 1000000) - 0.01))
                        self.browser.find_element_by_class_name('bid-input').send_keys(str(current_bid + 1))
                        self.browser.find_element_by_id('jsActiveBidButton').click()

                        # won defaulting to 1, check this somehow
                        DataRepository.create_history(url, (current_bid + 1 + auction_details['extra_costs']), 1, 1)
                        DataRepository.bought_item_on_wishlist(url, (current_bid + 1 + auction_details['extra_costs']))

                        # Close the window and quit this loop
                        self.browser.close()
                        break

                    time.sleep(0.05)
                    now = datetime.datetime.now()

                else:
                    print("Current bid is too high.")
                    print("Price: %s, max price: %s" % (
                        current_bid + auction_details['extra_costs'],
                        max_price
                    ))

                    DataRepository.create_history(url, (current_bid + auction_details['extra_costs']), 0, 0)
                    self.wait_for_next(url, max_price, auction_details['deadline'])

            except Exception as ex:
                print("Failed because of error: %s" % ex)
                self.wait_for_next(url, max_price, auction_details['deadline'])

    def wait_for_next(self, url, max_price, deadline):
        # wait until current auction is over
        now = datetime.datetime.now()

        if now < deadline:
            time_until_deadline = deadline - datetime.datetime.now()
            print("trying again in %s seconds" % time_until_deadline.seconds)

            time.sleep(abs(time_until_deadline.seconds + 20))
        else:
            time.sleep(20)

        # Revisit auction
        self.buy(url, max_price)

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
        time.sleep(3)

        auction_details = {
            'extra_costs': self.get_extra_cost(),
            'retail_price': self.get_retail_price(),
            'supplier_link': self.get_supplier_link(),
            'category': self.get_category(),
        }
        
        try:
            DataRepository.create_category(auction_details['category'], '', 0)
        except Exception:
            pass
        
        try:
            DataRepository.update_auction(
                url,
                auction_details['extra_costs'],
                auction_details['retail_price'],
                auction_details['category'],
                auction_details['supplier_link']
            )

        except Exception:
            try:
                DataRepository.create_auction(
                    url,
                    auction_details['extra_costs'],
                    auction_details['retail_price'],
                    auction_details['category'],
                    auction_details['supplier_link']
                )
            except Exception:
                pass

        return auction_details

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
            return 0

    def quit(self):
        self.browser.close()

    @staticmethod
    def check_credentials(username):
        with open('./data/credentials.json', 'r') as f:
            data = json.load(f)

        return data.get(username, None)

    @staticmethod
    def get_deadline(auction_block):
        try:
            bidding_container = auction_block.find_element_by_id('jsBiddingContainer')
            list_of_time = bidding_container.find_element_by_class_name('display-time-value').text.split(':')
            current_time = datetime.datetime.now()

            return current_time + datetime.timedelta(
                hours=int(list_of_time[0]), minutes=int(list_of_time[1]), seconds=int(list_of_time[2])
            )

        except Exception:
            try:
                countdown_label = auction_block.find_element_by_class_name('timer-countdown-label')
                return datetime.datetime.now() + datetime.timedelta(seconds=int(countdown_label.text))

            except Exception:
                return None

    @staticmethod
    def price_to_float(price_text):
        try:
            # make sure there's always .00 at the end for regex to match
            return float(re.search('\d+,\d+', '%s,00' % price_text).group(0).replace(',', '.'))

        except Exception:
            return None
