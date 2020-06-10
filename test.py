from models.VakantieveilingenController import VakantieveilingenController
from models.DataRepository import DataRepository
from threading import Thread

import json
import math


def check_auctions(controller):
    auctions = controller.explore_products(5)
    for auction in auctions:
        auction.update(controller.process_auction(auction['url']))
        print(auction)
        if auction['category'] not in blacklist['categories']:
            print("might buy, highest bid: €%.2f" % math.ceil(
                0.25 * auction['retail_price'] - auction['extra_costs']
            ))
            details = controller.fetch_auction_details(auction['url'])
            print(details)
            break
        else:
            print("Skip - Bad category")

        print("-" * 20)


def start_bidding(item):
    item_controller = VakantieveilingenController()
    if item_controller.login("simonvdhende@outlook.com"):
        item_controller.buy(
            item.get('AuctionURL'),
            item.get('MaxPrice')
        )


def main():
    # Fetch blacklist
    with open('./data/blacklist.json', 'r') as f:
        blacklist = json.load(f)

    threads = False
    if threads:
        for item in DataRepository.get_wishlist():
            # Start a thread for each item in the wishlist and try to buy said item
            item_thread = Thread(target=start_bidding, args=(item,))
            item_thread.start()

    else:
        # Contact vakantieveiligen
        controller = VakantieveilingenController()
        if controller.login("simonvdhende@outlook.com"):
            # Authentication successfull

            controller.buy(
                'https://www.vakantieveilingen.be/producten/elektronica/nordland_personenweegshaal-pd8734.html',
                25
            )

        # check_auctions(controller)


if __name__ == '__main__':
    main()
