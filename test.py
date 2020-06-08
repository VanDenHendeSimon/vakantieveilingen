from models.VakantieveilingenController import VakantieveilingenController
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


def main():
    # Fetch blacklist
    with open('./data/blacklist.json', 'r') as f:
        blacklist = json.load(f)

    # Contact vakantieveiligen
    controller = VakantieveilingenController()
    if controller.login("simonvdhende@outlook.com"):
        # Authentication successfull
        controller.buy(
            'https://www.vakantieveilingen.be/producten/elektronica/aircooler-mobiel_nedis-wit.html',
            35
        )

        # check_auctions(controller)


if __name__ == '__main__':
    main()
