from models.VakantieveilingenController import VakantieveilingenController
import json
import math


def main():
    # Fetch blacklist
    with open('./data/blacklist.json', 'r') as f:
        blacklist = json.load(f)

    # Contact vakantieveiligen
    controller = VakantieveilingenController()
    if controller.login("simonvdhende@outlook.com"):
        # Authentication successfull

        auctions = controller.explore_products(5)
        for auction in auctions:
            auction.update(controller.process_auction(auction))
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

        print("DONE")


if __name__ == '__main__':
    main()
